# Camada de repositorio: so acesso a banco, sem regra de negocio. Quem decide a
# ordem (criar pedido -> adicionar itens -> baixar estoque) e estoque_service.py.
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


def _com_itens_e_produto(stmt):
    # Encadeia o eager load dos itens e, pra cada item, do produto associado -
    # sem isso, ler item.produto fora da sessao async (ex: serializando ItemPedidoRead)
    # dispara lazy-load e quebra, porque a sessao ja fechou.
    return stmt.options(selectinload(Pedido.itens).selectinload(ItemPedido.produto))


async def get_by_id(db: AsyncSession, pedido_id: int) -> Pedido | None:
    result = await db.execute(_com_itens_e_produto(select(Pedido).where(Pedido.id == pedido_id)))
    return result.scalar_one_or_none()


async def list_pedidos(db: AsyncSession) -> list[Pedido]:
    """Pedidos mais recentes primeiro - e o que interessa pro painel interno.
    Ordena por id (nao por criado_em): o id e sempre estritamente crescente na
    ordem de criacao, enquanto `criado_em` pode empatar entre pedidos criados
    na mesma fracao de segundo (reparamos isso com SQLite nos testes, onde o
    timestamp so tem resolucao de segundo)."""
    result = await db.execute(_com_itens_e_produto(select(Pedido).order_by(Pedido.id.desc())))
    return list(result.scalars().all())
