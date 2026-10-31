from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import get_settings


@lru_cache
def get_llm() -> ChatOpenAI:
    """Mesmo padrao de LLM do wmsbox-agent (Hugging Face via roteador compativel
    com a API da OpenAI), mas o token vem de pydantic-settings, nunca de
    os.getenv/dotenv cru. Cacheado, construido sob demanda - nunca no import."""
    settings = get_settings()
    return ChatOpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.huggingface_api_token,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
    )
