"""Ferramentas do agente.

Ponto de seguranca central do projeto: o LLM NUNCA gera SQL nem codigo Python pra
rodar. Ele so escolhe qual destas funcoes chamar e com quais argumentos (puros
dados, validados por Pydantic). Toda escrita no banco passa por
app.services.estoque_service, que e codigo deterministico nosso.
"""

from decimal import Decimal

from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.produto import Produto
from app.models.schemas import ItemPedidoCreate
from app.services import estoque_service
from app.services.exceptions import EstoqueInsuficienteError, ProdutoNaoEncontradoError


def _formatar_quantidade(valor: Decimal) -> str:
    """Numero puro, sem zero a mais e sem separador de milhar - um valor tipo
    Decimal('300.000') (3 casas decimais fixas da coluna NUMERIC) vira "300",
    nunca "300.000" ou "300 000". Isso importa porque "300.000" escrito por um
    LLM em portugues pode virar "trezentos mil" (ponto como separador de milhar)
    em vez de "trezentos" (ponto como casa decimal) - erro de 1000x no estoque.
    `:f` forca notacao de ponto fixo (nunca cientifica) antes do rstrip.
    """
    texto = f"{valor:f}"
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto


def _format_produtos(produtos: list[Produto]) -> str:
    """Texto simples pro LLM ler, nao JSON - o agente so precisa narrar isso pro
    usuario, nao processar a estrutura."""
    if not produtos:
        return "Nenhum produto encontrado com esses filtros."
    linhas = [
        f"- {p.sku} | {p.nome} | categoria: {p.categoria} | "
        f"estoque atual: {_formatar_quantidade(p.quantidade_atual)} {p.unidade_medida} | "
        f"minimo: {_formatar_quantidade(p.quantidade_minima)} {p.unidade_medida} | "
        f"preco unitario: R$ {p.preco_unitario}"
        for p in produtos
    ]
    return "\n".join(linhas)


def _format_estoque_insuficiente(itens) -> str:
    detalhes = "; ".join(
        f"{i.sku}: pedido {_formatar_quantidade(i.solicitado)}, "
        f"disponivel {_formatar_quantidade(i.disponivel)}"
        for i in itens
    )
    return f"Estoque insuficiente para concluir o pedido. Itens com falta: {detalhes}"


# Schemas de argumento de cada ferramenta - o LangChain usa a `description` de cada
# campo pra explicar ao LLM o que preencher ali, e valida o que o LLM mandou antes
# de a funcao da tool rodar (ex: barra `quantidade` <= 0 antes de chegar no service).
class ConsultarEstoqueArgs(BaseModel):
    sku: str | None = Field(default=None, description="SKU exato do produto, se souber.")
    categoria: str | None = Field(
        default=None, description="Categoria do produto (ex: bloco, cimento, areia, ferramenta)."
    )
    abaixo_do_minimo: bool = Field(
        default=False, description="Se True, lista so produtos com estoque abaixo do minimo."
    )


class ReporEstoqueArgs(BaseModel):
    sku: str = Field(description="SKU do produto que esta recebendo entrada de estoque.")
    quantidade: Decimal = Field(gt=0, description="Quantidade recebida do fornecedor.")
    fornecedor_nome: str = Field(description="Nome do fornecedor que entregou a mercadoria.")
    fornecedor_contato: str | None = Field(default=None, description="Telefone/e-mail do fornecedor, se informado.")
    motivo: str | None = Field(default=None, description="Observacao livre sobre essa reposicao.")


class RegistrarPedidoArgs(BaseModel):
    cliente_nome: str = Field(min_length=1, description="Nome do cliente que esta fazendo o pedido.")
    itens: list[ItemPedidoCreate] = Field(description="Lista de SKU + quantidade pedidos pelo cliente.")


def make_tools(db: AsyncSession) -> list[BaseTool]:
    """Factory chamada uma vez por request de chat - cada tool fecha sobre a
    AsyncSession daquele request, mantendo o limite de transacao por conversa
    alinhado com o ciclo de vida da sessao do FastAPI."""

    @tool("consultar_estoque", args_schema=ConsultarEstoqueArgs)
    async def consultar_estoque(
        sku: str | None = None,
        categoria: str | None = None,
        abaixo_do_minimo: bool = False,
    ) -> str:
        """Consulta o estoque atual de produtos, podendo filtrar por SKU exato,
        categoria, ou listar so os produtos abaixo do estoque minimo."""
        produtos = await estoque_service.consultar_estoque(
            db, sku=sku, categoria=categoria, abaixo_do_minimo=abaixo_do_minimo
        )
        return _format_produtos(produtos)

    @tool("registrar_pedido", args_schema=RegistrarPedidoArgs)
    async def registrar_pedido(cliente_nome: str, itens: list[ItemPedidoCreate]) -> str:
        """Registra um pedido de cliente, dando baixa no estoque. Confere se ha
        estoque suficiente para TODOS os itens antes de confirmar - se faltar
        algum, nada e alterado."""
        try:
            pedido = await estoque_service.registrar_pedido(db, cliente_nome=cliente_nome, itens=itens)
        except EstoqueInsuficienteError as erro:
            return _format_estoque_insuficiente(erro.itens)
        except ProdutoNaoEncontradoError as erro:
            return f"SKU nao encontrado: {erro.identificador}"
        itens_txt = ", ".join(f"{i.sku} x{_formatar_quantidade(i.quantidade)}" for i in itens)
        return f"Pedido #{pedido.id} confirmado para {cliente_nome}: {itens_txt}."

    @tool("repor_estoque", args_schema=ReporEstoqueArgs)
    async def repor_estoque(
        sku: str,
        quantidade: Decimal,
        fornecedor_nome: str,
        fornecedor_contato: str | None = None,
        motivo: str | None = None,
    ) -> str:
        """Registra entrada de estoque vinda de um fornecedor (reposicao)."""
        try:
            produto = await estoque_service.repor_estoque(
                db,
                sku=sku,
                quantidade=quantidade,
                fornecedor_nome=fornecedor_nome,
                fornecedor_contato=fornecedor_contato,
                motivo=motivo,
            )
        except ProdutoNaoEncontradoError as erro:
            return f"SKU nao encontrado: {erro.identificador}"
        return (
            f"Estoque de {produto.sku} atualizado: "
            f"{_formatar_quantidade(produto.quantidade_atual)} {produto.unidade_medida}."
        )

    return [consultar_estoque, registrar_pedido, repor_estoque]
