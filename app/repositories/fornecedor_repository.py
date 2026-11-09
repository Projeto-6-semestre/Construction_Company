# Camada de repositorio: so acesso a banco, sem regra de negocio.
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fornecedor import Fornecedor


async def get_by_nome(db: AsyncSession, nome: str) -> Fornecedor | None:
    """Compara ignorando maiusculas/espacos nas pontas, pra "Fornecedor X" e
    " fornecedor x" nao virarem dois cadastros diferentes."""
    result = await db.execute(
        select(Fornecedor).where(func.lower(Fornecedor.nome) == nome.strip().lower())
    )
    return result.scalar_one_or_none()


async def get_or_create(db: AsyncSession, nome: str, contato: str | None = None) -> Fornecedor:
    """Usado na reposicao de estoque: se o fornecedor com esse nome ja existe,
    reusa; se nao, cadastra na hora - o usuario nao precisa cadastrar fornecedor
    numa tela separada antes de repor estoque."""
    fornecedor = await get_by_nome(db, nome)
    if fornecedor is not None:
        return fornecedor
    fornecedor = Fornecedor(nome=nome.strip(), contato=contato)
    db.add(fornecedor)
    # flush (nao commit): grava no banco da transacao atual e gera o id, mas so
    # fica permanente quando a transacao inteira der commit (ver estoque_service.py).
    await db.flush()
    return fornecedor
