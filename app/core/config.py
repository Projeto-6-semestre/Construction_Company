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

    database_url: str

    huggingface_api_token: str
    llm_model: str = "Qwen/Qwen2.5-72B-Instruct"
    llm_base_url: str = "https://router.huggingface.co/v1"
    llm_temperature: float = 0.0

    cors_allow_origins: list[str] = ["http://localhost:3000"]

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
