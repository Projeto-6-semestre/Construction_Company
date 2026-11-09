# Testes da camada de servico de autenticacao (painel interno), sem banco real -
# SQLite em memoria (ver tests/unit/conftest.py).
import pytest

from app.core.security import decodificar_access_token
from app.services import auth_service
from tests.unit.conftest import make_usuario


@pytest.mark.asyncio
async def test_autenticar_com_credenciais_corretas_retorna_usuario(db_session):
    usuario = make_usuario(username="admin", senha="senha-forte-123")
    db_session.add(usuario)
    await db_session.commit()

    resultado = await auth_service.autenticar(db_session, username="admin", senha="senha-forte-123")

    assert resultado is not None
    assert resultado.username == "admin"


@pytest.mark.asyncio
async def test_autenticar_com_senha_errada_retorna_none(db_session):
    usuario = make_usuario(username="admin", senha="senha-forte-123")
    db_session.add(usuario)
    await db_session.commit()

    resultado = await auth_service.autenticar(db_session, username="admin", senha="senha-errada")

    assert resultado is None


@pytest.mark.asyncio
async def test_autenticar_com_username_inexistente_retorna_none(db_session):
    resultado = await auth_service.autenticar(db_session, username="nao-existe", senha="qualquer")

    assert resultado is None


@pytest.mark.asyncio
async def test_gerar_token_produz_jwt_que_decodifica_pro_usuario_certo(db_session):
    usuario = make_usuario(username="admin", senha="senha-forte-123")
    db_session.add(usuario)
    await db_session.commit()
    await db_session.refresh(usuario)

    token = auth_service.gerar_token(usuario)
    payload = decodificar_access_token(token)

    assert payload["sub"] == str(usuario.id)
    assert payload["username"] == "admin"
