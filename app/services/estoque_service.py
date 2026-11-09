# Camada de servico: regra de negocio do estoque. E AQUI, e so aqui, que o estoque
# muda de verdade - repositories so sabem gravar/ler, nao decidem nada; o agente de IA
# (app/agent/tools.py) so chama essas funcoes, nunca grava no banco direto.
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import StatusPedido, TipoMovimentacao
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.schemas import (
    CategoriaResumoRead,
    DashboardRead,
    ItemPedidoCreate,
    ProdutoCreate,
    ProdutoUpdate,
)
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
    SkuJaExisteError,
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


async def listar_catalogo(
    db: AsyncSession,
    *,
    categoria: str | None = None,
    page: int = 1,
    page_size: int = 12,
) -> tuple[list[Produto], int]:
    """Vitrine publica paginada."""
    return await produto_repository.list_produtos_paginado(
        db, categoria=categoria, page=page, page_size=page_size
    )


async def listar_categorias(db: AsyncSession) -> list[str]:
    """So repassa pro repository - existe aqui pra API nunca chamar o repository
    direto, sempre passando pela camada de servico."""
    return await produto_repository.list_categorias(db)


async def listar_pedidos(db: AsyncSession) -> list[Pedido]:
    """Pedidos feitos pela loja (painel interno acompanhar). So repassa pro
    repository, mesma razao de listar_categorias."""
    return await pedido_repository.list_pedidos(db)


async def obter_dashboard(db: AsyncSession, *, limite_recentes: int = 30) -> DashboardRead:
    """Resumo de entrada/saida pro painel: totais gerais, quebra por categoria
    (valor estimado = quantidade * preco ATUAL do produto, ja que a movimentacao
    nao guarda o preco de quando aconteceu) e as movimentacoes mais recentes.

    Soma tudo em Python (nao em SQL agregado) de proposito: pro volume de dados
    de um projeto como esse, e muito mais simples de escrever certo e de testar
    do que um GROUP BY com CASE condicional, sem custo real de performance.
    """
    movimentacoes = await movimentacao_repository.list_todas(db)

    total_entradas_qtd = Decimal(0)
    total_saidas_qtd = Decimal(0)
    valor_entradas = Decimal(0)
    valor_saidas = Decimal(0)
    por_categoria: dict[str, dict[str, Decimal]] = {}

    for mov in movimentacoes:
        valor = mov.quantidade * mov.produto.preco_unitario
        categoria = por_categoria.setdefault(
            mov.produto.categoria, {"valor_entradas": Decimal(0), "valor_saidas": Decimal(0)}
        )
        if mov.tipo == TipoMovimentacao.ENTRADA:
            total_entradas_qtd += mov.quantidade
            valor_entradas += valor
            categoria["valor_entradas"] += valor
        else:
            total_saidas_qtd += mov.quantidade
            valor_saidas += valor
            categoria["valor_saidas"] += valor

    return DashboardRead(
        total_entradas_qtd=total_entradas_qtd,
        total_saidas_qtd=total_saidas_qtd,
        valor_entradas=valor_entradas,
        valor_saidas=valor_saidas,
        por_categoria=[
            CategoriaResumoRead(categoria=nome, **valores)
            for nome, valores in sorted(por_categoria.items())
        ],
        recentes=movimentacoes[:limite_recentes],
    )


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


async def criar_produto(db: AsyncSession, dados: ProdutoCreate) -> Produto:
    """Cadastro de produto novo (painel interno). Confere SKU duplicado antes de
    inserir porque e mais claro pro usuario do que deixar o banco rejeitar pela
    constraint `unique=True` do model."""
    try:
        existente = await produto_repository.get_by_sku(db, dados.sku)
        if existente is not None:
            raise SkuJaExisteError(dados.sku)

        produto = await produto_repository.criar(db, **dados.model_dump())
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(produto)
    return produto


async def atualizar_produto(db: AsyncSession, produto_id: int, dados: ProdutoUpdate) -> Produto:
    """Edita cadastro/preco de um produto existente - nunca mexe em
    quantidade_atual (esse campo so muda via registrar_pedido/repor_estoque)."""
    try:
        produto = await produto_repository.get_by_id(db, produto_id)
        if produto is None:
            raise ProdutoNaoEncontradoError(f"id={produto_id}")

        # exclude_unset: so aplica os campos que vieram de verdade no payload -
        # permite inclusive limpar a promocao mandando preco_promocional: null
        # de proposito, sem mexer nos campos que o cliente nao enviou.
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(produto, campo, valor)

        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(produto)
    return produto
