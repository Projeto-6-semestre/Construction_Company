from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import StatusPedido

if TYPE_CHECKING:
    from app.models.item_pedido import ItemPedido


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_nome: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[StatusPedido] = mapped_column(
        Enum(
            StatusPedido,
            name="status_pedido_enum",
            native_enum=True,
            # Grava o .value ("confirmado") em vez do nome do membro Python
            # ("CONFIRMADO") - precisa bater com os valores que a migration
            # usou pra criar o tipo ENUM nativo do Postgres.
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=StatusPedido.CONFIRMADO,
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido", cascade="all, delete-orphan")
