# Rota publica (sem login) pra registrar pedido direto, sem passar pelo chat -
# mesma regra de negocio do estoque_service que a tool do agente usa.
from fastapi import APIRouter, HTTPException

from app.api.deps import AdminUser, DbSession
from app.models.schemas import PedidoCreate, PedidoRead
from app.services import estoque_service
from app.services.exceptions import EstoqueInsuficienteError, ProdutoNaoEncontradoError

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("", response_model=list[PedidoRead])
async def listar_pedidos(db: DbSession, _admin: AdminUser) -> list[PedidoRead]:
    """Pedidos feitos na loja, mais recentes primeiro - painel interno
    acompanhar o que os clientes compraram. Exige login."""
    return await estoque_service.listar_pedidos(db)


@router.post("", response_model=PedidoRead, status_code=201)
async def criar_pedido(payload: PedidoCreate, db: DbSession) -> PedidoRead:
    """Caminho direto (sem chat) pra registrar um pedido - mesma regra de negocio
    que a ferramenta `registrar_pedido` do agente usa."""
    try:
        pedido = await estoque_service.registrar_pedido(
            db, cliente_nome=payload.cliente_nome, itens=payload.itens
        )
    except ProdutoNaoEncontradoError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except EstoqueInsuficienteError as erro:
        detalhe = [
            {"sku": i.sku, "solicitado": str(i.solicitado), "disponivel": str(i.disponivel)}
            for i in erro.itens
        ]
        raise HTTPException(status_code=409, detail=detalhe) from erro
    return pedido
