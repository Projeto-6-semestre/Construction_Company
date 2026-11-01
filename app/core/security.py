"""Hash de senha e tokens JWT do painel interno.

Sem framework de apresentacao aqui dentro (so bcrypt/jwt), seguindo o mesmo
principio do core/config.py - essa camada nao sabe nada de FastAPI.
"""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import get_settings

ALGORITMO = "HS256"


def hash_senha(senha_plana: str) -> str:
    return bcrypt.hashpw(senha_plana.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_plana: str, password_hash: str) -> bool:
    return bcrypt.checkpw(senha_plana.encode("utf-8"), password_hash.encode("utf-8"))


def criar_access_token(*, usuario_id: int, username: str) -> str:
    settings = get_settings()
    agora = datetime.now(UTC)
    payload = {
        "sub": str(usuario_id),
        "username": username,
        "iat": agora,
        "exp": agora + timedelta(minutes=settings.jwt_expiracao_minutos),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITMO)


def decodificar_access_token(token: str) -> dict:
    """Levanta jwt.PyJWTError (ou subclasses, ex: ExpiredSignatureError) se
    invalido/expirado - quem chama decide como traduzir isso pra HTTP 401."""
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITMO])
