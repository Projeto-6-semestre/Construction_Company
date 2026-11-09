# Excecoes de dominio da camada de servico. As rotas da API (app/api/routes/*.py)
# capturam essas excecoes e convertem pra status HTTP (404, 409, etc.); as tools do
# agente (app/agent/tools.py) capturam e devolvem como texto pro LLM explicar ao usuario.
from decimal import Decimal
from typing import NamedTuple


class ProdutoNaoEncontradoError(Exception):
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"Produto com SKU '{sku}' nao encontrado.")


class SkuJaExisteError(Exception):
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"Ja existe um produto com o SKU '{sku}'.")


class ItemFaltante(NamedTuple):
    sku: str
    solicitado: Decimal
    disponivel: Decimal


class EstoqueInsuficienteError(Exception):
    """Carrega TODOS os itens que faltam (nao so o primeiro) - quem chama consegue
    relatar o problema completo de uma vez, em vez de o usuario corrigir um item
    por vez e descobrir o proximo erro numa nova tentativa."""

    def __init__(self, itens: list[ItemFaltante]):
        self.itens = itens
        resumo = ", ".join(f"{i.sku} (pediu {i.solicitado}, tem {i.disponivel})" for i in itens)
        super().__init__(f"Estoque insuficiente para: {resumo}")
