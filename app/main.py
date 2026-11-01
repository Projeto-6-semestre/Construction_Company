from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, chat, health, pedidos, produtos
from app.core.config import get_settings
from app.core.db import dispose_engine
from app.core.logging import configure_logging
from app.services.exceptions import EstoqueInsuficienteError, ProdutoNaoEncontradoError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(title="Agente de Estoque - Materiais de Construcao", lifespan=lifespan)

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
    app.include_router(chat.router)

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
# efeito colateral no import que o CLAUDE.md evita (aquele era "carregar CSV e
# montar o agente de IA ja ao importar") - aqui so registra rotas; engine do banco
# e cliente do LLM continuam atras de factories com lru_cache, nunca construidos aqui.
app = create_app()
