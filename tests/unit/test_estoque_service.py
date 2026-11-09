# Testes da camada de servico (regra de negocio do estoque), sem banco real nem LLM -
# usam SQLite em memoria (ver tests/unit/conftest.py). Cobrem o caminho feliz e os
# casos em que o pedido PRECISA falhar sem alterar nada no meio do caminho.
from decimal import Decimal

import pytest
from sqlalchemy import select

from app.models.item_pedido import ItemPedido
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.models.pedido import Pedido
from app.models.schemas import ItemPedidoCreate, PedidoRead, ProdutoCreate, ProdutoUpdate
from app.services import estoque_service
from app.services.exceptions import (
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
    SkuJaExisteError,
)
from tests.unit.conftest import make_produto


async def _contar(db, model) -> int:
    """Conta quantas linhas existem de um model - usado pra confirmar que nada foi
    criado quando um pedido devia falhar por completo."""
    result = await db.execute(select(model))
    return len(result.scalars().all())


@pytest.mark.asyncio
async def test_registrar_pedido_com_estoque_suficiente_decrementa_corretamente(db_session):
    produto = make_produto(sku="BLOCO-09", quantidade_atual=100)
    db_session.add(produto)
    await db_session.commit()

    pedido = await estoque_service.registrar_pedido(
        db_session,
        cliente_nome="Joao da Silva",
        itens=[ItemPedidoCreate(sku="BLOCO-09", quantidade=Decimal(30))],
    )

    assert pedido.id is not None
    assert len(pedido.itens) == 1

    await db_session.refresh(produto)
    assert produto.quantidade_atual == Decimal(70)

    assert await _contar(db_session, ItemPedido) == 1
    movimentacoes = (await db_session.execute(select(MovimentacaoEstoque))).scalars().all()
    assert len(movimentacoes) == 1
    assert movimentacoes[0].tipo.value == "saida"
    assert movimentacoes[0].quantidade == Decimal(30)


@pytest.mark.asyncio
async def test_registrar_pedido_com_estoque_insuficiente_levanta_erro_e_nao_altera_nada(db_session):
    produto = make_produto(sku="CIMENTO-50KG", quantidade_atual=10)
    db_session.add(produto)
    await db_session.commit()

    with pytest.raises(EstoqueInsuficienteError) as exc_info:
        await estoque_service.registrar_pedido(
            db_session,
            cliente_nome="Maria Souza",
            itens=[ItemPedidoCreate(sku="CIMENTO-50KG", quantidade=Decimal(50))],
        )

    assert exc_info.value.itens[0].sku == "CIMENTO-50KG"
    assert exc_info.value.itens[0].solicitado == Decimal(50)
    assert exc_info.value.itens[0].disponivel == Decimal(10)

    await db_session.refresh(produto)
    assert produto.quantidade_atual == Decimal(10)
    assert await _contar(db_session, Pedido) == 0
    assert await _contar(db_session, ItemPedido) == 0
    assert await _contar(db_session, MovimentacaoEstoque) == 0


@pytest.mark.asyncio
async def test_registrar_pedido_com_multiplos_itens_so_confirma_se_todos_tiverem_estoque(db_session):
    produto_ok = make_produto(sku="AREIA-M3", quantidade_atual=100)
    produto_faltando = make_produto(sku="FERRAMENTA-X", quantidade_atual=2)
    db_session.add_all([produto_ok, produto_faltando])
    await db_session.commit()

    with pytest.raises(EstoqueInsuficienteError) as exc_info:
        await estoque_service.registrar_pedido(
            db_session,
            cliente_nome="Construtora ABC",
            itens=[
                ItemPedidoCreate(sku="AREIA-M3", quantidade=Decimal(10)),
                ItemPedidoCreate(sku="FERRAMENTA-X", quantidade=Decimal(5)),
            ],
        )

    # So o item que realmente falta estoque aparece na lista de faltantes.
    skus_faltantes = {item.sku for item in exc_info.value.itens}
    assert skus_faltantes == {"FERRAMENTA-X"}

    # Nada foi alterado, nem o produto que tinha estoque suficiente.
    await db_session.refresh(produto_ok)
    await db_session.refresh(produto_faltando)
    assert produto_ok.quantidade_atual == Decimal(100)
    assert produto_faltando.quantidade_atual == Decimal(2)
    assert await _contar(db_session, Pedido) == 0


@pytest.mark.asyncio
async def test_registrar_pedido_com_sku_inexistente_levanta_erro(db_session):
    with pytest.raises(ProdutoNaoEncontradoError):
        await estoque_service.registrar_pedido(
            db_session,
            cliente_nome="Cliente Qualquer",
            itens=[ItemPedidoCreate(sku="SKU-QUE-NAO-EXISTE", quantidade=Decimal(1))],
        )

    assert await _contar(db_session, Pedido) == 0


@pytest.mark.asyncio
async def test_repor_estoque_incrementa_corretamente(db_session):
    produto = make_produto(sku="TELHA-CERAMICA", quantidade_atual=20)
    db_session.add(produto)
    await db_session.commit()

    atualizado = await estoque_service.repor_estoque(
        db_session,
        sku="TELHA-CERAMICA",
        quantidade=Decimal(15),
        fornecedor_nome="Ceramica Forte Ltda",
    )

    assert atualizado.quantidade_atual == Decimal(35)

    movimentacoes = (await db_session.execute(select(MovimentacaoEstoque))).scalars().all()
    assert len(movimentacoes) == 1
    assert movimentacoes[0].tipo.value == "entrada"
    assert movimentacoes[0].quantidade == Decimal(15)
    assert movimentacoes[0].fornecedor_id is not None


@pytest.mark.asyncio
async def test_listar_pedidos_traz_mais_recente_primeiro_com_produto_aninhado(db_session):
    produto = make_produto(sku="BLOCO-09", nome="Bloco de concreto 9 furos", quantidade_atual=100)
    db_session.add(produto)
    await db_session.commit()

    primeiro = await estoque_service.registrar_pedido(
        db_session, cliente_nome="Joao", itens=[ItemPedidoCreate(sku="BLOCO-09", quantidade=Decimal(5))]
    )
    segundo = await estoque_service.registrar_pedido(
        db_session, cliente_nome="Maria", itens=[ItemPedidoCreate(sku="BLOCO-09", quantidade=Decimal(3))]
    )

    pedidos = await estoque_service.listar_pedidos(db_session)

    assert [p.id for p in pedidos] == [segundo.id, primeiro.id]

    # Serializa com o schema de resposta da API de verdade - confirma que o
    # eager load (Pedido.itens -> ItemPedido.produto) é suficiente pra isso não
    # estourar lazy-load fora da sessão, e que o nome/sku do produto aparece.
    lido = PedidoRead.model_validate(pedidos[0])
    assert lido.itens[0].produto.sku == "BLOCO-09"
    assert lido.itens[0].produto.nome == "Bloco de concreto 9 furos"


@pytest.mark.asyncio
async def test_obter_dashboard_soma_entradas_e_saidas_por_categoria(db_session):
    bloco = make_produto(
        sku="BLOCO-09", categoria="bloco", quantidade_atual=100, preco_unitario=Decimal(2)
    )
    cimento = make_produto(
        sku="CIMENTO-50KG", categoria="cimento", quantidade_atual=100, preco_unitario=Decimal(40)
    )
    db_session.add_all([bloco, cimento])
    await db_session.commit()

    # Saida: 10 blocos a R$2 = R$20.
    await estoque_service.registrar_pedido(
        db_session, cliente_nome="Cliente X", itens=[ItemPedidoCreate(sku="BLOCO-09", quantidade=Decimal(10))]
    )
    # Entrada: 5 sacos de cimento a R$40 = R$200.
    await estoque_service.repor_estoque(
        db_session, sku="CIMENTO-50KG", quantidade=Decimal(5), fornecedor_nome="Fornecedor Y"
    )

    dashboard = await estoque_service.obter_dashboard(db_session)

    assert dashboard.total_saidas_qtd == Decimal(10)
    assert dashboard.total_entradas_qtd == Decimal(5)
    assert dashboard.valor_saidas == Decimal(20)
    assert dashboard.valor_entradas == Decimal(200)

    por_categoria = {c.categoria: c for c in dashboard.por_categoria}
    assert por_categoria["bloco"].valor_saidas == Decimal(20)
    assert por_categoria["bloco"].valor_entradas == Decimal(0)
    assert por_categoria["cimento"].valor_entradas == Decimal(200)
    assert por_categoria["cimento"].valor_saidas == Decimal(0)

    assert len(dashboard.recentes) == 2


@pytest.mark.asyncio
async def test_listar_catalogo_pagina_corretamente_e_devolve_total_geral(db_session):
    # Nomes escolhidos de proposito pra ordem alfabetica ficar previsivel
    # (list_produtos_paginado ordena por Produto.nome).
    db_session.add_all(
        [
            make_produto(sku="AREIA-01", nome="Areia Grossa", categoria="areia"),
            make_produto(sku="BLOCO-01", nome="Bloco 10x20", categoria="bloco"),
            make_produto(sku="CIMENTO-01", nome="Cimento CP2", categoria="cimento"),
        ]
    )
    await db_session.commit()

    pagina_1, total = await estoque_service.listar_catalogo(db_session, page=1, page_size=2)
    assert total == 3
    assert [p.sku for p in pagina_1] == ["AREIA-01", "BLOCO-01"]

    pagina_2, total = await estoque_service.listar_catalogo(db_session, page=2, page_size=2)
    assert total == 3
    assert [p.sku for p in pagina_2] == ["CIMENTO-01"]


@pytest.mark.asyncio
async def test_listar_catalogo_filtra_por_categoria(db_session):
    db_session.add_all(
        [
            make_produto(sku="BLOCO-01", nome="Bloco 10x20", categoria="bloco"),
            make_produto(sku="FERRAMENTA-01", nome="Martelo", categoria="ferramenta"),
        ]
    )
    await db_session.commit()

    itens, total = await estoque_service.listar_catalogo(db_session, categoria="ferramenta")
    assert total == 1
    assert [p.sku for p in itens] == ["FERRAMENTA-01"]


@pytest.mark.asyncio
async def test_listar_categorias_retorna_distintas_sem_repetir(db_session):
    db_session.add_all(
        [
            make_produto(sku="BLOCO-01", nome="Bloco 10x20", categoria="bloco"),
            make_produto(sku="BLOCO-02", nome="Bloco 14x20", categoria="bloco"),
            make_produto(sku="CIMENTO-01", nome="Cimento CP2", categoria="cimento"),
        ]
    )
    await db_session.commit()

    categorias = await estoque_service.listar_categorias(db_session)
    assert categorias == ["bloco", "cimento"]


@pytest.mark.asyncio
async def test_criar_produto_cadastra_corretamente(db_session):
    dados = ProdutoCreate(
        sku="TELHA-01",
        nome="Telha Ceramica",
        categoria="telha",
        unidade_medida="un",
        quantidade_atual=Decimal(50),
        quantidade_minima=Decimal(5),
        preco_unitario=Decimal(10),
    )

    produto = await estoque_service.criar_produto(db_session, dados)

    assert produto.id is not None
    assert produto.sku == "TELHA-01"
    assert produto.quantidade_atual == Decimal(50)
    assert await _contar(db_session, type(produto)) == 1


@pytest.mark.asyncio
async def test_criar_produto_com_sku_duplicado_levanta_erro_e_nao_cria_outro(db_session):
    produto_existente = make_produto(sku="BLOCO-09")
    db_session.add(produto_existente)
    await db_session.commit()

    dados = ProdutoCreate(
        sku="BLOCO-09",
        nome="Bloco Duplicado",
        categoria="bloco",
        unidade_medida="un",
        preco_unitario=Decimal(5),
    )

    with pytest.raises(SkuJaExisteError):
        await estoque_service.criar_produto(db_session, dados)

    assert await _contar(db_session, type(produto_existente)) == 1


@pytest.mark.asyncio
async def test_atualizar_produto_edita_so_campos_enviados_e_preserva_resto(db_session):
    produto = make_produto(
        sku="BLOCO-09",
        nome="Bloco de concreto 9 furos",
        categoria="bloco",
        quantidade_atual=100,
        preco_unitario=2,
    )
    db_session.add(produto)
    await db_session.commit()

    # So preco_unitario e enviado - exclude_unset faz o resto ficar intocado,
    # inclusive quantidade_atual (que nem existe no schema ProdutoUpdate).
    atualizado = await estoque_service.atualizar_produto(
        db_session, produto.id, ProdutoUpdate(preco_unitario=Decimal(99))
    )

    assert atualizado.preco_unitario == Decimal(99)
    assert atualizado.nome == "Bloco de concreto 9 furos"
    assert atualizado.categoria == "bloco"
    assert atualizado.quantidade_atual == Decimal(100)


@pytest.mark.asyncio
async def test_atualizar_produto_com_id_inexistente_levanta_erro(db_session):
    with pytest.raises(ProdutoNaoEncontradoError):
        await estoque_service.atualizar_produto(
            db_session, 999999, ProdutoUpdate(preco_unitario=Decimal(10))
        )
