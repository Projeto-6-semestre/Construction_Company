from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario


async def get_by_username(db: AsyncSession, username: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, usuario_id: int) -> Usuario | None:
    return await db.get(Usuario, usuario_id)
