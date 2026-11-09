# Schemas Pydantic: o "formato" de dado que entra e sai da API (nao confundir com os
# models de app/models/*.py, que sao as tabelas do banco via SQLAlchemy). FastAPI usa
# essas classes pra validar requisicao e gerar a documentacao automatica em /docs.
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import StatusPedido, TipoMovimentacao

# --- Produto ---


class ProdutoRead(BaseModel):
    """O que a API devolve ao consultar um produto. `from_attributes=True` deixa
    o Pydantic ler direto de um objeto SQLAlchemy (model Produto), sem precisar
    converter campo a campo manualmente."""


    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    nome: str
    categoria: str
    unidade_medida: str
    quantidade_atual: Decimal
    quantidade_minima: Decimal
    preco_unitario: Decimal
    preco_promocional: Decimal | None
    imagem_url: str | None
    criado_em: datetime
    atualizado_em: datetime


class ProdutoPage(BaseModel):
    """Resposta paginada do catalogo (loja publica e painel interno) - `total` e o
    total geral (nao so dessa pagina), usado pelo front pra montar a paginacao."""

    items: list[ProdutoRead]
    total: int
    page: int
    page_size: int


class ProdutoCreate(BaseModel):
    """Corpo de POST /produtos (cadastro). `quantidade_atual` aqui e so o estoque
    inicial no cadastro - depois disso so muda via pedido/reposicao."""

    sku: str
    nome: str
    categoria: str
    unidade_medida: str
    quantidade_atual: Decimal = Field(ge=0, default=Decimal(0))
    quantidade_minima: Decimal = Field(ge=0, default=Decimal(0))
    preco_unitario: Decimal = Field(gt=0)
    preco_promocional: Decimal | None = Field(default=None, gt=0)
    imagem_url: str | None = None


class ProdutoUpdate(BaseModel):
    """Edita cadastro/preco - nunca quantidade_atual direto (isso so muda via
    pedido/reposicao, pra nao furar o historico de movimentacoes)."""

    nome: str | None = None
    categoria: str | None = None
    unidade_medida: str | None = None
    quantidade_minima: Decimal | None = Field(default=None, ge=0)
    preco_unitario: Decimal | None = Field(default=None, gt=0)
    preco_promocional: Decimal | None = Field(default=None, gt=0)
    imagem_url: str | None = None


# --- Pedido ---


class ItemPedidoCreate(BaseModel):
    """Um item dentro do corpo de POST /pedidos - identifica o produto pelo SKU
    (nao pelo id interno), porque e isso que o cliente/front conhece."""

    sku: str
    quantidade: Decimal = Field(gt=0)


class ProdutoResumoRead(BaseModel):
    """Versao enxuta do produto, so pra exibir dentro de um item de pedido no
    painel (nome/sku) - sem repetir o schema inteiro de ProdutoRead."""

    model_config = ConfigDict(from_attributes=True)

    sku: str
    nome: str


class ItemPedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    quantidade: Decimal
    produto: ProdutoResumoRead


class PedidoCreate(BaseModel):
    """Corpo de POST /pedidos. `min_length=1` barra pedido vazio direto na validacao,
    antes mesmo de chegar na camada de servico."""

    cliente_nome: str
    itens: list[ItemPedidoCreate] = Field(min_length=1)


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_nome: str
    status: StatusPedido
    criado_em: datetime
    itens: list[ItemPedidoRead]


class ItemFaltanteRead(BaseModel):
    """Usado na resposta 409 (estoque insuficiente) - lista TODOS os itens que
    faltaram de uma vez, nao so o primeiro, pra quem pediu corrigir tudo junto."""

    sku: str
    solicitado: Decimal
    disponivel: Decimal


# --- Chat (agente de IA) ---


class ChatMessage(BaseModel):
    """Uma mensagem do historico da conversa, mandada de volta pro backend a cada
    pergunta nova pra dar contexto ao agente (o backend nao guarda sessao de chat)."""

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    pergunta: str
    historico: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    resposta: str


# --- Autenticacao (painel interno) ---


class LoginRequest(BaseModel):
    username: str
    senha: str


class TokenResponse(BaseModel):
    """Resposta do login - o front guarda `access_token` e manda em
    `Authorization: Bearer <token>` nas rotas protegidas do painel."""

    access_token: str
    token_type: str = "bearer"


# --- Dashboard (entradas/saidas de estoque) ---


class FornecedorResumoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str


class MovimentacaoEstoqueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoMovimentacao
    quantidade: Decimal
    motivo: str | None
    criado_em: datetime
    produto: ProdutoResumoRead
    fornecedor: FornecedorResumoRead | None


class CategoriaResumoRead(BaseModel):
    """Entradas x saidas somadas por categoria, em valor estimado (quantidade
    vezes o PRECO ATUAL do produto - a movimentacao nao guarda o preco de quando
    aconteceu, entao isso e uma aproximacao, nao um valor contabil exato)."""

    categoria: str
    valor_entradas: Decimal
    valor_saidas: Decimal


class DashboardRead(BaseModel):
    """Resumo pro painel: totais gerais, quebra por categoria (pro grafico) e as
    movimentacoes mais recentes (pra tabela de historico)."""

    total_entradas_qtd: Decimal
    total_saidas_qtd: Decimal
    valor_entradas: Decimal
    valor_saidas: Decimal
    por_categoria: list[CategoriaResumoRead]
    recentes: list[MovimentacaoEstoqueRead]
