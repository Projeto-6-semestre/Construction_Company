# Camada de repositorio: so acesso a banco, sem regra de negocio.
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

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
