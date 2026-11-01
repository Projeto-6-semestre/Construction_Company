"""Popula o banco com produtos de demonstracao (blocos, cimento, areia, ferramentas).

Uso:
    uv run python scripts/seed_data.py

Idempotente: produtos cujo SKU ja existe sao pulados, nao duplicados.
"""

import asyncio
from decimal import Decimal

from app.core.db import get_session_maker
from app.models.produto import Produto
from app.repositories import produto_repository

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
    dict(sku="TIJOLO-6FUROS", nome="Tijolo ceramico 6 furos", categoria="bloco",
         unidade_medida="un", quantidade_atual=Decimal(3000), quantidade_minima=Decimal(300),
         preco_unitario=Decimal("0.95")),
    dict(sku="CAL-HIDRATADA-20KG", nome="Cal hidratada saco 20kg", categoria="cimento",
         unidade_medida="saco", quantidade_atual=Decimal(150), quantidade_minima=Decimal(30),
         preco_unitario=Decimal("14.50")),
    dict(sku="ARGAMASSA-ACII-20KG", nome="Argamassa colante ACII saco 20kg", categoria="cimento",
         unidade_medida="saco", quantidade_atual=Decimal(200), quantidade_minima=Decimal(40),
         preco_unitario=Decimal("22.00")),
    dict(sku="PEDRISCO-M3", nome="Pedrisco", categoria="brita",
         unidade_medida="m3", quantidade_atual=Decimal(30), quantidade_minima=Decimal(8),
         preco_unitario=Decimal("88.00")),
    dict(sku="FERRO-10MM-BARRA", nome="Vergalhao de ferro 10mm, barra 12m", categoria="ferragem",
         unidade_medida="un", quantidade_atual=Decimal(250), quantidade_minima=Decimal(40),
         preco_unitario=Decimal("62.00")),
    dict(sku="FERRO-8MM-BARRA", nome="Vergalhao de ferro 8mm, barra 12m", categoria="ferragem",
         unidade_medida="un", quantidade_atual=Decimal(300), quantidade_minima=Decimal(40),
         preco_unitario=Decimal("48.00")),
    dict(sku="ARAME-RECOZIDO-KG", nome="Arame recozido 18 BWG", categoria="ferragem",
         unidade_medida="kg", quantidade_atual=Decimal(80), quantidade_minima=Decimal(15),
         preco_unitario=Decimal("12.00")),
    dict(sku="TINTA-LATEX-18L", nome="Tinta latex PVA branca, lata 18L", categoria="tinta",
         unidade_medida="lata", quantidade_atual=Decimal(60), quantidade_minima=Decimal(10),
         preco_unitario=Decimal("210.00")),
    dict(sku="FERRAMENTA-TROWEL", nome="Desempenadeira dentada", categoria="ferramenta",
         unidade_medida="un", quantidade_atual=Decimal(25), quantidade_minima=Decimal(5),
         preco_unitario=Decimal("32.00")),
    dict(sku="FERRAMENTA-CARRINHO", nome="Carrinho de mao reforcado", categoria="ferramenta",
         unidade_medida="un", quantidade_atual=Decimal(18), quantidade_minima=Decimal(3),
         preco_unitario=Decimal("180.00")),
    dict(sku="TUBO-PVC-100MM", nome="Tubo de PVC esgoto 100mm, barra 6m", categoria="hidraulica",
         unidade_medida="un", quantidade_atual=Decimal(120), quantidade_minima=Decimal(20),
         preco_unitario=Decimal("55.00")),
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
