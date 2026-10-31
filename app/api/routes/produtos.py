from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.models.schemas import ProdutoRead
from app.repositories import produto_repository
from app.services import estoque_service

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("", response_model=list[ProdutoRead])
async def listar_produtos(
    db: DbSession,
    categoria: str | None = None,
    abaixo_do_minimo: bool = False,
) -> list[ProdutoRead]:
    """Lista o estoque atual - sem passar pelo LLM, pra alimentar a tabela do frontend."""
    produtos = await estoque_service.consultar_estoque(
        db, categoria=categoria, abaixo_do_minimo=abaixo_do_minimo
    )
    return produtos


@router.get("/{produto_id}", response_model=ProdutoRead)
async def obter_produto(produto_id: int, db: DbSession) -> ProdutoRead:
    produto = await produto_repository.get_by_id(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")
    return produto
