from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.produto import Produto


async def get_by_id(db: AsyncSession, produto_id: int) -> Produto | None:
    return await db.get(Produto, produto_id)


async def get_by_sku(db: AsyncSession, sku: str) -> Produto | None:
    result = await db.execute(select(Produto).where(Produto.sku == sku))
    return result.scalar_one_or_none()


async def get_by_sku_for_update(db: AsyncSession, sku: str) -> Produto | None:
    """SELECT ... FOR UPDATE - trava a linha ate o fim da transacao, evitando que
    dois pedidos simultaneos pro mesmo produto leiam a mesma quantidade disponivel."""
    result = await db.execute(select(Produto).where(Produto.sku == sku).with_for_update())
    return result.scalar_one_or_none()


async def list_produtos(
    db: AsyncSession,
    *,
    categoria: str | None = None,
    abaixo_do_minimo: bool = False,
) -> list[Produto]:
    stmt = select(Produto)
    if categoria is not None:
        stmt = stmt.where(Produto.categoria == categoria)
    if abaixo_do_minimo:
        stmt = stmt.where(Produto.quantidade_atual < Produto.quantidade_minima)
    stmt = stmt.order_by(Produto.nome)
    result = await db.execute(stmt)
    return list(result.scalars().all())


def aplicar_delta_quantidade(produto: Produto, delta: Decimal) -> None:
    """delta positivo = entrada, negativo = saida. So ajusta o objeto em memoria;
    quem decide commit/rollback e a camada de servico."""
    produto.quantidade_atual = produto.quantidade_atual + delta
