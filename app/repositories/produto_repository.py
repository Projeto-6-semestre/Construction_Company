from decimal import Decimal

from sqlalchemy import func, select
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


async def list_produtos_paginado(
    db: AsyncSession,
    *,
    categoria: str | None = None,
    page: int = 1,
    page_size: int = 12,
) -> tuple[list[Produto], int]:
    """Catalogo paginado pra vitrine publica - diferente de list_produtos (usada
    pelo agente, sem paginacao, porque o agente precisa do conjunto inteiro que
    bate o filtro pra responder certo, nao so uma pagina)."""
    stmt = select(Produto)
    count_stmt = select(func.count()).select_from(Produto)
    if categoria is not None:
        stmt = stmt.where(Produto.categoria == categoria)
        count_stmt = count_stmt.where(Produto.categoria == categoria)

    total = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.order_by(Produto.nome).offset((page - 1) * page_size).limit(page_size)
    itens = list((await db.execute(stmt)).scalars().all())
    return itens, total


async def list_categorias(db: AsyncSession) -> list[str]:
    stmt = select(Produto.categoria).distinct().order_by(Produto.categoria)
    result = await db.execute(stmt)
    return list(result.scalars().all())


def aplicar_delta_quantidade(produto: Produto, delta: Decimal) -> None:
    """delta positivo = entrada, negativo = saida. So ajusta o objeto em memoria;
    quem decide commit/rollback e a camada de servico."""
    produto.quantidade_atual = produto.quantidade_atual + delta


async def criar(db: AsyncSession, **campos) -> Produto:
    produto = Produto(**campos)
    db.add(produto)
    await db.flush()
    return produto
