from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.base import Base
from app.models.produto import Produto


@pytest_asyncio.fixture
async def db_session():
    """Banco SQLite em memoria, schema criado direto do metadata (sem Alembic) -
    rapido e sem infra externa. Testes de integracao (Postgres real) ficam em
    tests/integration/."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()


def make_produto(
    *,
    sku: str = "BLOCO-09",
    nome: str = "Bloco de concreto 9 furos",
    categoria: str = "bloco",
    unidade_medida: str = "un",
    quantidade_atual: Decimal | int = 100,
    quantidade_minima: Decimal | int = 10,
    preco_unitario: Decimal | int = 2,
) -> Produto:
    return Produto(
        sku=sku,
        nome=nome,
        categoria=categoria,
        unidade_medida=unidade_medida,
        quantidade_atual=Decimal(quantidade_atual),
        quantidade_minima=Decimal(quantidade_minima),
        preco_unitario=Decimal(preco_unitario),
    )
