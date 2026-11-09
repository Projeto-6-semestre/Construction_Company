from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.item_pedido import ItemPedido
    from app.models.movimentacao_estoque import MovimentacaoEstoque


class Produto(Base):
    """Um item do catalogo (ex: um SKU de bloco, cimento, areia, ferramenta).
    `quantidade_atual` e a fonte da verdade do estoque - so muda via
    services/estoque_service.py, nunca editada direto por uma rota de cadastro."""

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    unidade_medida: Mapped[str] = mapped_column(String(20), nullable=False)

    # Numeric(12, 3), nunca float - estoque e dinheiro/quantidade exigem precisao exata,
    # float introduziria erro de arredondamento com o tempo (ex: 0.1 + 0.2 != 0.3).
    quantidade_atual: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    # Abaixo desse valor o produto aparece como "estoque baixo" (ver produto_repository.py).
    quantidade_minima: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    # Se preenchido, e o preco que a loja publica mostra em vez do preco_unitario.
    preco_promocional: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    imagem_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    itens_pedido: Mapped[list["ItemPedido"]] = relationship(back_populates="produto")
    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(back_populates="produto")
