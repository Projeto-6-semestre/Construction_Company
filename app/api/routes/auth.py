from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.models.schemas import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    """Unica rota publica de autenticacao - devolve o JWT que o front usa nas
    rotas protegidas do painel (ver app/api/deps.py)."""
    usuario = await auth_service.autenticar(db, username=payload.username, senha=payload.senha)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos.")
    token = auth_service.gerar_token(usuario)
    return TokenResponse(access_token=token)
