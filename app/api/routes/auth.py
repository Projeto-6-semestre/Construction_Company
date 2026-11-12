from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.core import rate_limit
from app.models.schemas import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    """Unica rota publica de autenticacao - devolve o JWT que o front usa nas
    rotas protegidas do painel (ver app/api/deps.py).

    Bloqueia por `username` (nao por IP) apos muitas tentativas erradas
    seguidas - evita brute-force de senha sem precisar extrair IP real por
    trás do proxy do Render."""
    chave = payload.username.lower()
    if rate_limit.bloqueado(chave):
        raise HTTPException(
            status_code=429, detail="Muitas tentativas de login. Tente novamente em alguns minutos."
        )

    usuario = await auth_service.autenticar(db, username=payload.username, senha=payload.senha)
    if usuario is None:
        rate_limit.registrar_falha(chave)
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos.")

    rate_limit.limpar(chave)
    token = auth_service.gerar_token(usuario)
    return TokenResponse(access_token=token)
