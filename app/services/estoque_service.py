from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import StatusPedido, TipoMovimentacao
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.schemas import ItemPedidoCreate
from app.repositories import (
    fornecedor_repository,
    movimentacao_repository,
    pedido_repository,
    produto_repository,
)
from app.services.exceptions import (
    EstoqueInsuficienteError,
    ItemFaltante,
    ProdutoNaoEncontradoError,
)


async def consultar_estoque(
    db: AsyncSession,
    *,
    sku: str | None = None,
    categoria: str | None = None,
    abaixo_do_minimo: bool = False,
) -> list[Produto]:
    """Leitura pura, sem transacao - nao muda nada."""
    if sku is not None:
        produto = await produto_repository.get_by_sku(db, sku)
        return [produto] if produto is not None else []
    return await produto_repository.list_produtos(db, categoria=categoria, abaixo_do_minimo=abaixo_do_minimo)


async def registrar_pedido(
    db: AsyncSession,
    *,
    cliente_nome: str,
    itens: list[ItemPedidoCreate],
) -> Pedido:
    """Cria um pedido de cliente, baixando o estoque. Garante que ou TODOS os itens
    sao atendidos, ou NADA e alterado (sem baixa parcial de estoque): commit so no
    final, rollback em qualquer excecao no meio do caminho.
    """
    if not itens:
        raise ValueError("O pedido precisa ter pelo menos um item.")

    # Nao usa `async with db.begin()`: a AsyncSession do SQLAlchemy "autobegin" uma
    # transacao sozinha assim que a primeira query roda, e o agente reusa a mesma
    # sessao entre varias chamadas de ferramenta numa mesma conversa - chamar
    # `db.begin()` explicitamente nessas condicoes levanta "A transaction is
    # already begun". Em vez disso, deixamos o autobegin agir e controlamos
    # commit/rollback na mao, o que funciona tanto com quanto sem transacao previa.
    try:
        produtos_por_sku: dict[str, Produto] = {}
        faltantes: list[ItemFaltante] = []

        for item in itens:
            produto = await produto_repository.get_by_sku_for_update(db, item.sku)
            if produto is None:
                raise ProdutoNaoEncontradoError(item.sku)
            produtos_por_sku[item.sku] = produto
            if produto.quantidade_atual < item.quantidade:
                faltantes.append(
                    ItemFaltante(sku=item.sku, solicitado=item.quantidade, disponivel=produto.quantidade_atual)
                )

        if faltantes:
            raise EstoqueInsuficienteError(faltantes)

        pedido = await pedido_repository.create_pedido(
            db, cliente_nome=cliente_nome, status=StatusPedido.CONFIRMADO
        )

        for item in itens:
            produto = produtos_por_sku[item.sku]
            await pedido_repository.add_item(
                db, pedido_id=pedido.id, produto_id=produto.id, quantidade=item.quantidade
            )
            await movimentacao_repository.registrar(
                db,
                produto_id=produto.id,
                tipo=TipoMovimentacao.SAIDA,
                quantidade=item.quantidade,
                motivo=f"Pedido #{pedido.id} - {cliente_nome}",
            )
            produto_repository.aplicar_delta_quantidade(produto, -item.quantidade)

        await db.commit()
    except Exception:
        await db.rollback()
        raise

    pedido_completo = await pedido_repository.get_by_id(db, pedido.id)
    assert pedido_completo is not None
    return pedido_completo


async def repor_estoque(
    db: AsyncSession,
    *,
    sku: str,
    quantidade: Decimal,
    fornecedor_nome: str,
    fornecedor_contato: str | None = None,
    motivo: str | None = None,
) -> Produto:
    """Registra entrada de mercadoria vinda de um fornecedor."""
    if quantidade <= 0:
        raise ValueError("A quantidade reposta precisa ser maior que zero.")

    try:
        produto = await produto_repository.get_by_sku_for_update(db, sku)
        if produto is None:
            raise ProdutoNaoEncontradoError(sku)

        fornecedor = await fornecedor_repository.get_or_create(db, fornecedor_nome, fornecedor_contato)

        await movimentacao_repository.registrar(
            db,
            produto_id=produto.id,
            tipo=TipoMovimentacao.ENTRADA,
            quantidade=quantidade,
            motivo=motivo or f"Reposicao - {fornecedor_nome}",
            fornecedor_id=fornecedor.id,
        )
        produto_repository.aplicar_delta_quantidade(produto, quantidade)

        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(produto)
    return produto
