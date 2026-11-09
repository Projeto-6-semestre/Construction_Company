from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.movimentacao_estoque import MovimentacaoEstoque


class Fornecedor(Base):
    """Quem entrega material pra empresa (nao e cliente). Criado automaticamente
    (get_or_create) quando alguem repoe estoque informando um fornecedor novo -
    ver services/estoque_service.py."""

    __tablename__ = "fornecedores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    contato: Mapped[str | None] = mapped_column(String(200), nullable=True)

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(back_populates="fornecedor")
