# Enums compartilhados pelos models. Viram tipo ENUM nativo do Postgres na migration
# (ver movimentacao_estoque.py e pedido.py) - o banco recusa qualquer valor fora da lista,
# nao so o Python.
from enum import Enum


class TipoMovimentacao(str, Enum):
    """Toda entrada/saida de estoque tem um desses dois tipos."""

    ENTRADA = "entrada"
    SAIDA = "saida"


class StatusPedido(str, Enum):
    """Hoje todo pedido nasce CONFIRMADO (ver services/estoque_service.py) - nao tem
    fluxo de aprovacao manual nessa fase, mas o campo ja existe pra quando precisar."""

    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
