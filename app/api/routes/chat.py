# Rota que liga o painel interno ao agente de IA (app/agent/agent_service.py).
from fastapi import APIRouter

from app.agent import agent_service
from app.api.deps import AdminUser, DbSession
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: DbSession, _admin: AdminUser) -> ChatResponse:
    """Chat do agente - painel interno, exige login (nunca exposto a cliente anonimo)."""
    resposta = await agent_service.ask(db, payload.pergunta, payload.historico)
    return ChatResponse(resposta=resposta)
