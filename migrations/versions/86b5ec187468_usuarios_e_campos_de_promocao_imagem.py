"""usuarios e campos de promocao/imagem

Revision ID: 86b5ec187468
Revises: c03068e24e6d
Create Date: 2026-10-31 16:23:02.235017

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '86b5ec187468'
down_revision: str | Sequence[str] | None = 'c03068e24e6d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    Adiciona a tabela usuarios (login do painel interno) e os campos
    preco_promocional/imagem_url em produtos (pra loja publica).
    """
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_usuarios_username", "usuarios", ["username"], unique=True)

    op.add_column("produtos", sa.Column("preco_promocional", sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column("produtos", sa.Column("imagem_url", sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema - desfaz exatamente o que upgrade() fez."""
    op.drop_column("produtos", "imagem_url")
    op.drop_column("produtos", "preco_promocional")

    op.drop_index("ix_usuarios_username", table_name="usuarios")
    op.drop_table("usuarios")
