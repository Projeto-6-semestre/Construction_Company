"""Popula o banco com produtos de demonstracao (blocos, cimento, areia, ferramentas).

Uso:
    uv run python scripts/seed_data.py

Idempotente: produtos cujo SKU ja existe sao pulados, nao duplicados.
"""

import asyncio
from decimal import Decimal

from app.core.db import get_session_maker
from app.repositories import produto_repository
from app.models.produto import Produto

PRODUTOS_DEMO = [
    dict(sku="BLOCO-09", nome="Bloco de concreto 9 furos", categoria="bloco",
         unidade_medida="un", quantidade_atual=Decimal(1200), quantidade_minima=Decimal(200),
         preco_unitario=Decimal("2.50")),
    dict(sku="BLOCO-14", nome="Bloco de concreto 14 furos", categoria="bloco",
         unidade_medida="un", quantidade_atual=Decimal(800), quantidade_minima=Decimal(150),
         preco_unitario=Decimal("3.20")),
    dict(sku="CIMENTO-50KG", nome="Cimento CP-II saco 50kg", categoria="cimento",
         unidade_medida="saco", quantidade_atual=Decimal(300), quantidade_minima=Decimal(50),
         preco_unitario=Decimal("38.90")),
    dict(sku="AREIA-M3", nome="Areia media lavada", categoria="areia",
         unidade_medida="m3", quantidade_atual=Decimal(60), quantidade_minima=Decimal(10),
         preco_unitario=Decimal("85.00")),
    dict(sku="BRITA-M3", nome="Brita 1", categoria="brita",
         unidade_medida="m3", quantidade_atual=Decimal(45), quantidade_minima=Decimal(10),
         preco_unitario=Decimal("95.00")),
    dict(sku="FERRAMENTA-COLHER", nome="Colher de pedreiro", categoria="ferramenta",
         unidade_medida="un", quantidade_atual=Decimal(40), quantidade_minima=Decimal(5),
         preco_unitario=Decimal("18.00")),
    dict(sku="FERRAMENTA-NIVEL", nome="Nivel de bolha 60cm", categoria="ferramenta",
         unidade_medida="un", quantidade_atual=Decimal(15), quantidade_minima=Decimal(3),
         preco_unitario=Decimal("45.00")),
    dict(sku="TELHA-CERAMICA", nome="Telha ceramica colonial", categoria="telha",
         unidade_medida="un", quantidade_atual=Decimal(5000), quantidade_minima=Decimal(500),
         preco_unitario=Decimal("1.80")),
]


async def main() -> None:
    session_maker = get_session_maker()
    async with session_maker() as db:
        criados = 0
        for dados in PRODUTOS_DEMO:
            existente = await produto_repository.get_by_sku(db, dados["sku"])
            if existente is not None:
                print(f"- {dados['sku']} ja existe, pulando")
                continue
            db.add(Produto(**dados))
            criados += 1
            print(f"+ {dados['sku']} criado")
        await db.commit()
    print(f"\n{criados} produto(s) novo(s) criado(s).")


if __name__ == "__main__":
    asyncio.run(main())
