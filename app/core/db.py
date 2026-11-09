from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Conexao com o banco (PostgreSQL via SQLAlchemy async). Tudo atras de factories com
# lru_cache - a engine/sessionmaker so sao criadas na primeira vez que alguem pede,
# nunca so por importar este modulo (evita o anti-padrao de efeito colateral no import).
from app.core.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    """Uma unica engine (pool de conexoes) reusada pra aplicacao inteira."""
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=settings.debug, future=True)


@lru_cache
def get_session_maker() -> async_sessionmaker[AsyncSession]:
    # expire_on_commit=False: depois do commit, os objetos continuam acessiveis sem
    # disparar uma query nova (importante porque os services leem o objeto de volta
    # logo apos o commit, ex: devolver o produto atualizado pra API).
    return async_sessionmaker(bind=get_engine(), expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Dependencia do FastAPI: uma sessao por request, sem transacao implicita aberta.
    Quem abre `async with db.begin()` e a camada de servico, nao esta funcao."""
    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session


async def dispose_engine() -> None:
    """Chamado no shutdown da aplicacao (lifespan)."""
    if get_engine.cache_info().currsize:
        await get_engine().dispose()
