from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import get_settings


@lru_cache
def get_llm() -> ChatOpenAI:
    """Groq, via endpoint compativel com a API da OpenAI - tier gratuito sem
    cartao, bom suporte a tool-calling multi-etapa (llama-3.3-70b-versatile).
    Token vem de pydantic-settings, nunca de os.getenv/dotenv cru. Cacheado,
    construido sob demanda - nunca no import."""
    settings = get_settings()
    return ChatOpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.groq_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
    )
