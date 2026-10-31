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
    criado_em: datetime
    atualizado_em: datetime


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
