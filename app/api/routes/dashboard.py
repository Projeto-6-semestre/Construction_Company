# Resumo de entradas/saidas de estoque pro painel interno (grafico + tabela).
from fastapi import APIRouter

from app.api.deps import AdminUser, DbSession
from app.models.schemas import DashboardRead
from app.services import estoque_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardRead)
async def obter_dashboard(db: DbSession, _admin: AdminUser) -> DashboardRead:
    """Totais de entrada/saida, quebra por categoria e movimentacoes recentes.
    Exige login - mesma regra das outras telas do painel interno."""
    return await estoque_service.obter_dashboard(db)
