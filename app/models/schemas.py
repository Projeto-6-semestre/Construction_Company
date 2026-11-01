from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import StatusPedido


class ProdutoRead(BaseModel):
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
    items: list[ProdutoRead]
    total: int
    page: int
    page_size: int


class ProdutoCreate(BaseModel):
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


class ItemPedidoCreate(BaseModel):
    sku: str
    quantidade: Decimal = Field(gt=0)


class ItemPedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    quantidade: Decimal


class PedidoCreate(BaseModel):
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
    sku: str
    solicitado: Decimal
    disponivel: Decimal


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    pergunta: str
    historico: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    resposta: str


class LoginRequest(BaseModel):
    username: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
