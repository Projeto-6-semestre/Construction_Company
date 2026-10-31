from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=settings.debug, future=True)


@lru_cache
def get_session_maker() -> async_sessionmaker[AsyncSession]:
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
