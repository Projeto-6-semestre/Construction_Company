"""Cria (ou reseta a senha de) um usuario do painel interno.

Nao existe cadastro publico de proposito - so quem tem acesso ao servidor/banco
consegue criar login novo, igual o setup.php do projeto de referencia.

Uso:
    uv run python scripts/criar_admin.py <username> <senha>
"""

import asyncio
import sys

from app.core.db import get_session_maker
from app.core.security import hash_senha
from app.models.usuario import Usuario
from app.repositories import usuario_repository


async def main(username: str, senha: str) -> None:
    session_maker = get_session_maker()
    async with session_maker() as db:
        existente = await usuario_repository.get_by_username(db, username)
        if existente is not None:
            existente.password_hash = hash_senha(senha)
            await db.commit()
            print(f"Senha do usuario '{username}' atualizada.")
            return

        usuario = Usuario(username=username, password_hash=hash_senha(senha))
        db.add(usuario)
        await db.commit()
        print(f"Usuario '{username}' criado.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: uv run python scripts/criar_admin.py <username> <senha>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
