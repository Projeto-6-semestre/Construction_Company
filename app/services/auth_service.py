from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import criar_access_token, verificar_senha
from app.models.usuario import Usuario
from app.repositories import usuario_repository


async def autenticar(db: AsyncSession, *, username: str, senha: str) -> Usuario | None:
    """Retorna o usuario se username+senha baterem, None caso contrario.
    Resposta identica (None) tanto pra usuario inexistente quanto senha errada -
    nao da pra quem tenta logar descobrir se o username existe."""
    usuario = await usuario_repository.get_by_username(db, username)
    if usuario is None:
        return None
    if not verificar_senha(senha, usuario.password_hash):
        return None
    return usuario


def gerar_token(usuario: Usuario) -> str:
    return criar_access_token(usuario_id=usuario.id, username=usuario.username)
