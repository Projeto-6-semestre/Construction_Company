# Camada de repositorio: so acesso a banco, sem regra de negocio.
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import TipoMovimentacao
from app.models.movimentacao_estoque import MovimentacaoEstoque


async def registrar(
    db: AsyncSession,
    *,
    produto_id: int,
    tipo: TipoMovimentacao,
    quantidade: Decimal,
    motivo: str | None = None,
    fornecedor_id: int | None = None,
) -> MovimentacaoEstoque:
    """Grava uma linha no historico de entrada/saida - e isso que fica como
    auditoria de tudo que mexeu no estoque, mesmo que o produto mude depois."""
    movimentacao = MovimentacaoEstoque(
        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo,
        fornecedor_id=fornecedor_id,
    )
    db.add(movimentacao)
    await db.flush()
    return movimentacao


async def list_todas(db: AsyncSession) -> list[MovimentacaoEstoque]:
    """Todo o historico de entrada/saida, mais recente primeiro - base pro
    dashboard (resumo e tabela). Ordena por id, nao por criado_em, pelo mesmo
    motivo do pedido_repository: timestamps podem empatar no mesmo segundo."""
    result = await db.execute(
        select(MovimentacaoEstoque)
        .options(selectinload(MovimentacaoEstoque.produto), selectinload(MovimentacaoEstoque.fornecedor))
        .order_by(MovimentacaoEstoque.id.desc())
    )
    return list(result.scalars().all())
