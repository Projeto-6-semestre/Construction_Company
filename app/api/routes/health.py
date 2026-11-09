# Rota simples sem autenticacao, so pra checar se a API esta no ar (usada em
# deploy/monitoramento, nao tem relacao com estoque).
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
