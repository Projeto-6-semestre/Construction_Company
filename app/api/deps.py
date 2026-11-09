from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import decodificar_access_token
from app.models.usuario import Usuario
from app.repositories import usuario_repository

# Atalho de tipo: qualquer rota que declare um parametro `db: DbSession` recebe
# uma AsyncSession pronta (FastAPI resolve via Depends/get_db automaticamente).
DbSession = Annotated[AsyncSession, Depends(get_db)]

# auto_error=False: deixamos a propria funcao abaixo decidir a mensagem/status de
# erro quando falta token, em vez do erro generico padrao do HTTPBearer.
_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_usuario(
    db: DbSession,
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
) -> Usuario:
    """Dependencia pro painel interno - exige 'Authorization: Bearer <token>'.
    Usada nas rotas que so funcionario/dono da empresa deve acessar (chat,
    lista de estoque do painel, cadastro/edicao de produto)."""
    if credenciais is None:
        raise HTTPException(status_code=401, detail="Nao autenticado.")

    try:
        payload = decodificar_access_token(credenciais.credentials)
    except jwt.PyJWTError as erro:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado.") from erro

    usuario = await usuario_repository.get_by_id(db, int(payload["sub"]))
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado.")
    return usuario


# Atalho de tipo: `_admin: AdminUser` num parametro de rota basta pra exigir login -
# FastAPI roda get_current_usuario antes do corpo da rota e barra quem nao passar.
AdminUser = Annotated[Usuario, Depends(get_current_usuario)]

__all__ = ["AdminUser", "DbSession", "get_db"]
