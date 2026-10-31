from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import StatusPedido
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido


async def create_pedido(db: AsyncSession, *, cliente_nome: str, status: StatusPedido) -> Pedido:
    pedido = Pedido(cliente_nome=cliente_nome, status=status)
    db.add(pedido)
    await db.flush()
    return pedido


async def add_item(db: AsyncSession, *, pedido_id: int, produto_id: int, quantidade: Decimal) -> ItemPedido:
    item = ItemPedido(pedido_id=pedido_id, produto_id=produto_id, quantidade=quantidade)
    db.add(item)
    await db.flush()
    return item


async def get_by_id(db: AsyncSession, pedido_id: int) -> Pedido | None:
    result = await db.execute(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    return result.scalar_one_or_none()
