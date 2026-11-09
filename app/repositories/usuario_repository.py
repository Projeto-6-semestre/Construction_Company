# Camada de repositorio: so acesso direto ao banco (SELECT/INSERT via SQLAlchemy),
# sem nenhuma regra de negocio - quem decide o que fazer com o resultado e a camada
# de servico/API que chama essas funcoes.
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario


async def get_by_username(db: AsyncSession, username: str) -> Usuario | None:
    """Usado no login - username e unico, entao ou acha um ou nao acha nenhum."""
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, usuario_id: int) -> Usuario | None:
    return await db.get(Usuario, usuario_id)
