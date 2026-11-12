# Testes no nivel HTTP (via ASGI, sem subir servidor de verdade) - os testes de
# app/services/*.py so chamam a funcao Python direto, nunca passaram pela API.
# Esses aqui confirmam o que a API de verdade devolve: status code certo,
# rota protegida barrando quem nao manda token, e o rate limit do login.
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.db import get_db
from app.main import create_app
from tests.unit.conftest import make_usuario


@pytest.fixture
def app(db_session):
    """App FastAPI de verdade, mas com `get_db` trocado pela sessao SQLite em
    memoria do teste - nunca toca um banco real nem precisa do .env completo
    alem do que o Settings() ja exige pra instanciar."""
    aplicacao = create_app()

    async def _get_db_override():
        yield db_session

    aplicacao.dependency_overrides[get_db] = _get_db_override
    return aplicacao


@pytest.mark.asyncio
async def test_login_com_credenciais_corretas_retorna_token(app, db_session):
    db_session.add(make_usuario(username="admin-http", senha="senha-correta-123"))
    await db_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resposta = await client.post(
            "/auth/login", json={"username": "admin-http", "senha": "senha-correta-123"}
        )

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()


@pytest.mark.asyncio
async def test_login_com_senha_errada_retorna_401(app, db_session):
    db_session.add(make_usuario(username="admin-401", senha="senha-correta-123"))
    await db_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resposta = await client.post("/auth/login", json={"username": "admin-401", "senha": "errada"})

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_rota_protegida_sem_token_retorna_401(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resposta = await client.get("/produtos")

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_payload_invalido_retorna_422(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # username vazio - Field(min_length=1) deve barrar antes de chegar no service.
        resposta = await client.post("/auth/login", json={"username": "", "senha": "x"})

    assert resposta.status_code == 422


@pytest.mark.asyncio
async def test_login_bloqueia_apos_muitas_tentativas_erradas(app, db_session):
    db_session.add(make_usuario(username="usuario-bloqueio", senha="senha-correta-123"))
    await db_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for _ in range(5):
            resposta = await client.post(
                "/auth/login", json={"username": "usuario-bloqueio", "senha": "errada"}
            )
            assert resposta.status_code == 401

        # 6a tentativa, mesmo com a senha CERTA, deve ser barrada pelo rate limit.
        resposta = await client.post(
            "/auth/login", json={"username": "usuario-bloqueio", "senha": "senha-correta-123"}
        )

    assert resposta.status_code == 429
