from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracao tipada do app. Nao importa nada de apresentacao (nem FastAPI,
    nem framework de frontend) - so dados de configuracao."""

    env: Literal["local", "homologacao", "producao"] = "local"
    debug: bool = True

    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # String de conexao assincrona do SQLAlchemy, ex:
    # postgresql+asyncpg://usuario:senha@host:5432/banco
    database_url: str

    # Credenciais/config do provedor de LLM (Groq, endpoint compativel com a API da
    # OpenAI) usado pelo agente de IA em app/agent/llm.py.
    groq_api_key: str
    llm_model: str = "openai/gpt-oss-120b"
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_temperature: float = 0.0

    cors_allow_origins: list[str] = ["http://localhost:3000"]

    # Autenticacao do painel interno (funcionarios/dono da empresa).
    jwt_secret: str
    jwt_expiracao_minutos: int = 480

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value):
        """Aceita tanto JSON (["a","b"]) quanto uma lista separada por virgula no .env."""
        if isinstance(value, str) and not value.strip().startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Cacheado, mas construido sob demanda - nunca no import do modulo."""
    return Settings()
