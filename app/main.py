# Ponto unico de entrada da aplicacao: monta o FastAPI, registra as rotas de cada
# camada da API, CORS e os tratadores de excecao de dominio. `uvicorn app.main:app`
# aponta pra esse arquivo.
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, chat, dashboard, health, pedidos, produtos
from app.core.config import get_settings
from app.core.db import dispose_engine
from app.core.logging import configure_logging
from app.services.exceptions import EstoqueInsuficienteError, ProdutoNaoEncontradoError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Roda em volta da vida inteira da aplicacao: o `yield` e onde o FastAPI fica
    servindo requests; so depois dele (shutdown) e que fecha a engine do banco."""
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    """Factory da aplicacao - nada e construido no nivel do modulo antes de alguem
    chamar isso (nem settings, nem rotas), seguindo o mesmo principio de
    inicializacao explicita das factories de app/core/db.py e app/agent/llm.py."""
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(title="Agente de Estoque - Materiais de Construcao", lifespan=lifespan)

    # CORS restrito ao frontend local; allow_credentials=False porque essa fase nao
    # usa cookie de sessao (autenticacao e via header Authorization: Bearer).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(produtos.router)
    app.include_router(pedidos.router)
    app.include_router(dashboard.router)
    app.include_router(chat.router)

    # Converte excecoes de dominio (levantadas em services/estoque_service.py) em
    # respostas HTTP, sem cada rota precisar de try/except repetido pra isso.
    @app.exception_handler(ProdutoNaoEncontradoError)
    async def produto_nao_encontrado_handler(request: Request, exc: ProdutoNaoEncontradoError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(EstoqueInsuficienteError)
    async def estoque_insuficiente_handler(request: Request, exc: EstoqueInsuficienteError):
        itens = [
            {"sku": i.sku, "solicitado": str(i.solicitado), "disponivel": str(i.disponivel)}
            for i in exc.itens
        ]
        return JSONResponse(status_code=409, content={"detail": itens})

    return app


# Modulo-level pra `uvicorn app.main:app` funcionar. Isso NAO e o anti-padrao de
# efeito colateral no import (projeto de referencia carregava CSV e montava o
# agente de IA ja ao importar) - aqui so registra rotas; engine do banco
# e cliente do LLM continuam atras de factories com lru_cache, nunca construidos aqui.
app = create_app()
