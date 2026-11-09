"""initial schema

Revision ID: c03068e24e6d
Revises:
Create Date: 2026-10-26 21:58:37.445279

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c03068e24e6d'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    Cria as 5 tabelas iniciais do projeto: fornecedores, produtos, pedidos,
    itens_pedido e movimentacoes_estoque (nessa ordem, por causa das FKs).
    """
    op.create_table(
        "fornecedores",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("contato", sa.String(length=200), nullable=True),
    )

    op.create_table(
        "produtos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.Column("categoria", sa.String(length=100), nullable=False),
        sa.Column("unidade_medida", sa.String(length=20), nullable=False),
        sa.Column("quantidade_atual", sa.Numeric(precision=12, scale=3), nullable=False, server_default="0"),
        sa.Column("quantidade_minima", sa.Numeric(precision=12, scale=3), nullable=False, server_default="0"),
        sa.Column("preco_unitario", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_produtos_sku", "produtos", ["sku"], unique=True)

    status_pedido_enum = sa.Enum("pendente", "confirmado", "cancelado", name="status_pedido_enum")
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cliente_nome", sa.String(length=200), nullable=False),
        sa.Column("status", status_pedido_enum, nullable=False, server_default="confirmado"),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "itens_pedido",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "pedido_id",
            sa.Integer(),
            sa.ForeignKey("pedidos.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "produto_id",
            sa.Integer(),
            sa.ForeignKey("produtos.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=3), nullable=False),
    )
    op.create_index("ix_itens_pedido_pedido_id", "itens_pedido", ["pedido_id"])
    op.create_index("ix_itens_pedido_produto_id", "itens_pedido", ["produto_id"])

    tipo_movimentacao_enum = sa.Enum("entrada", "saida", name="tipo_movimentacao_enum")
    op.create_table(
        "movimentacoes_estoque",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "produto_id",
            sa.Integer(),
            sa.ForeignKey("produtos.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("tipo", tipo_movimentacao_enum, nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("motivo", sa.String(length=300), nullable=True),
        sa.Column(
            "fornecedor_id",
            sa.Integer(),
            sa.ForeignKey("fornecedores.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_movimentacoes_estoque_produto_id", "movimentacoes_estoque", ["produto_id"])
    op.create_index("ix_movimentacoes_estoque_criado_em", "movimentacoes_estoque", ["criado_em"])


def downgrade() -> None:
    """Downgrade schema - desfaz exatamente o que upgrade() fez, incluindo os
    tipos ENUM nativos do Postgres (drop_table sozinho NAO remove o CREATE TYPE)."""
    op.drop_index("ix_movimentacoes_estoque_criado_em", table_name="movimentacoes_estoque")
    op.drop_index("ix_movimentacoes_estoque_produto_id", table_name="movimentacoes_estoque")
    op.drop_table("movimentacoes_estoque")

    op.drop_index("ix_itens_pedido_produto_id", table_name="itens_pedido")
    op.drop_index("ix_itens_pedido_pedido_id", table_name="itens_pedido")
    op.drop_table("itens_pedido")

    op.drop_table("pedidos")

    op.drop_index("ix_produtos_sku", table_name="produtos")
    op.drop_table("produtos")

    op.drop_table("fornecedores")

    sa.Enum(name="tipo_movimentacao_enum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="status_pedido_enum").drop(op.get_bind(), checkfirst=True)
