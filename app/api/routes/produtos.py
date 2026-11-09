from fastapi import APIRouter, HTTPException, Query

from app.api.deps import AdminUser, DbSession
from app.models.schemas import ProdutoCreate, ProdutoPage, ProdutoRead, ProdutoUpdate
from app.repositories import produto_repository
from app.services import estoque_service
from app.services.exceptions import ProdutoNaoEncontradoError, SkuJaExisteError

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("", response_model=list[ProdutoRead])
async def listar_produtos(
    db: DbSession,
    _admin: AdminUser,
    categoria: str | None = None,
    abaixo_do_minimo: bool = False,
) -> list[ProdutoRead]:
    """Lista o estoque atual pro painel interno - exige login (nao e usada pela loja)."""
    produtos = await estoque_service.consultar_estoque(
        db, categoria=categoria, abaixo_do_minimo=abaixo_do_minimo
    )
    return produtos


@router.get("/categorias", response_model=list[str])
async def listar_categorias(db: DbSession) -> list[str]:
    """Categorias existentes de verdade no catalogo - publica, usada pela vitrine."""
    return await estoque_service.listar_categorias(db)


@router.get("/catalogo", response_model=ProdutoPage)
async def listar_catalogo(
    db: DbSession,
    categoria: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=100),
) -> ProdutoPage:
    """Vitrine publica paginada - usada pela loja (frontend/app/loja)."""
    itens, total = await estoque_service.listar_catalogo(
        db, categoria=categoria, page=page, page_size=page_size
    )
    return ProdutoPage(items=itens, total=total, page=page, page_size=page_size)


@router.post("", response_model=ProdutoRead, status_code=201)
async def criar_produto(payload: ProdutoCreate, db: DbSession, _admin: AdminUser) -> ProdutoRead:
    """Cadastra produto novo - painel interno, exige login."""
    try:
        return await estoque_service.criar_produto(db, payload)
    except SkuJaExisteError as erro:
        raise HTTPException(status_code=409, detail=str(erro)) from erro


@router.patch("/{produto_id}", response_model=ProdutoRead)
async def atualizar_produto(
    produto_id: int, payload: ProdutoUpdate, db: DbSession, _admin: AdminUser
) -> ProdutoRead:
    """Edita nome/categoria/preco/promocao/imagem - nunca a quantidade em estoque
    direto (isso so muda via pedido ou reposicao, pra manter o historico certo).
    Painel interno, exige login."""
    try:
        return await estoque_service.atualizar_produto(db, produto_id, payload)
    except ProdutoNaoEncontradoError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro


@router.get("/{produto_id}", response_model=ProdutoRead)
async def obter_produto(produto_id: int, db: DbSession) -> ProdutoRead:
    """Detalhe de um produto por id - publica (pagina de produto da loja)."""
    produto = await produto_repository.get_by_id(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")
    return produto
