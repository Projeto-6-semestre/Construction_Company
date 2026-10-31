from fastapi import APIRouter

from app.agent import agent_service
from app.api.deps import DbSession
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: DbSession) -> ChatResponse:
    resposta = await agent_service.ask(db, payload.pergunta, payload.historico)
    return ChatResponse(resposta=resposta)
