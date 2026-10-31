from langchain.agents import create_agent
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.llm import get_llm
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import make_tools
from app.models.schemas import ChatMessage


def build_agent(db: AsyncSession):
    """Monta o agente pra UM request - inicializacao explicita, nunca um agente
    global criado no import do modulo (era exatamente esse o problema do
    wmsbox-agent, que carregava o CSV e montava o agente ja ao importar)."""
    return create_agent(model=get_llm(), tools=make_tools(db), system_prompt=SYSTEM_PROMPT)


async def ask(db: AsyncSession, pergunta: str, historico: list[ChatMessage] | None = None) -> str:
    agent = build_agent(db)

    messages = [{"role": m.role, "content": m.content} for m in (historico or [])]
    messages.append({"role": "user", "content": pergunta})

    resultado = await agent.ainvoke({"messages": messages})
    ultima_mensagem = resultado["messages"][-1]
    return ultima_mensagem.content
