from decimal import Decimal

import pytest
from sqlalchemy import select

from app.models.item_pedido import ItemPedido
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.models.pedido import Pedido
from app.models.schemas import ItemPedidoCreate
from app.services import estoque_service
from app.services.exceptions import EstoqueInsuficienteError, ProdutoNaoEncontradoError
from tests.unit.conftest import make_produto


async def _contar(db, model) -> int:
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
