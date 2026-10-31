from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fornecedor import Fornecedor


async def get_by_nome(db: AsyncSession, nome: str) -> Fornecedor | None:
    result = await db.execute(
        select(Fornecedor).where(func.lower(Fornecedor.nome) == nome.strip().lower())
    )
    return result.scalar_one_or_none()


async def get_or_create(db: AsyncSession, nome: str, contato: str | None = None) -> Fornecedor:
    fornecedor = await get_by_nome(db, nome)
    if fornecedor is not None:
        return fornecedor
    fornecedor = Fornecedor(nome=nome.strip(), contato=contato)
    db.add(fornecedor)
    await db.flush()
    return fornecedor
