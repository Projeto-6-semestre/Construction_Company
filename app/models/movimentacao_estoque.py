from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TipoMovimentacao

if TYPE_CHECKING:
    from app.models.fornecedor import Fornecedor
    from app.models.produto import Produto


class MovimentacaoEstoque(Base):
    """Historico/auditoria de toda entrada e saida - e o que garante que o sistema
    sempre sabe o numero certo de estoque, sem depender de contagem manual."""

    __tablename__ = "movimentacoes_estoque"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    tipo: Mapped[TipoMovimentacao] = mapped_column(
        Enum(
            TipoMovimentacao,
            name="tipo_movimentacao_enum",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    # Pra ENTRADA fica em branco normalmente; pra SAIDA costuma citar o pedido.
    motivo: Mapped[str | None] = mapped_column(String(300), nullable=True)
    # So preenchido em ENTRADA (de qual fornecedor veio o material). SET NULL: se o
    # fornecedor for removido, o historico da movimentacao continua existindo.
    fornecedor_id: Mapped[int | None] = mapped_column(
        ForeignKey("fornecedores.id", ondelete="SET NULL"), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    produto: Mapped["Produto"] = relationship(back_populates="movimentacoes")
    fornecedor: Mapped["Fornecedor | None"] = relationship(back_populates="movimentacoes")
