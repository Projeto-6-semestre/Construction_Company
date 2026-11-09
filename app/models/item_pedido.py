from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.produto import Produto


class ItemPedido(Base):
    """Uma linha dentro de um pedido: "tantas unidades desse produto". Um Pedido
    tem varios ItemPedido (relacao 1-pra-muitos, ver Pedido.itens)."""

    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # CASCADE: apagar o pedido apaga os itens dele junto (fazem parte do pedido).
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # RESTRICT: nao deixa apagar um produto que ja foi vendido em algum pedido,
    # pra nao perder o historico.
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # Numeric (nao float) porque e quantidade de estoque - arredondamento errado
    # aqui significaria contar material que nao existe ou perder material que existe.
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship(back_populates="itens_pedido")
