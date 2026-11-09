"use client";

import Image from "next/image";
import { iconeCategoria } from "@/lib/categorias";
import type { Produto } from "@/types/api";
import styles from "./ProductCard.module.css";

function formatarPreco(valor: string): string {
  return Number(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

interface Props {
  produto: Produto;
  onAdicionar: (produto: Produto) => void;
}

// Card de produto no catalogo da loja. Mostra preco promocional riscado (se
// tiver) e desabilita o botao de compra quando o estoque zerou.
export function ProductCard({ produto, onAdicionar }: Props) {
  const semEstoque = Number(produto.quantidade_atual) <= 0;
  const temPromocao = produto.preco_promocional !== null;
  // % de desconto calculado na hora (preco promo / preco normal), so pra exibir o selo.
  const percentualOff = temPromocao
    ? Math.round(
        (1 - Number(produto.preco_promocional) / Number(produto.preco_unitario)) * 100,
      )
    : 0;

  return (
    <div className={styles.card}>
      <div className={styles.imagem}>
        {produto.imagem_url ? (
          <Image
            src={produto.imagem_url}
            alt={produto.nome}
            fill
            sizes="200px"
            className={styles.imagemFoto}
            unoptimized
          />
        ) : (
          <span>{iconeCategoria(produto.categoria)}</span>
        )}
        {temPromocao && <span className={styles.selo}>-{percentualOff}%</span>}
      </div>
      <p className={styles.codigo}>Cód. {produto.sku}</p>
      <h3 className={styles.nome}>{produto.nome}</h3>
      {temPromocao ? (
        <p className={styles.preco}>
          <span className={styles.precoAntigo}>{formatarPreco(produto.preco_unitario)}</span>
          <span className={styles.precoPromo}>{formatarPreco(produto.preco_promocional!)}</span>
          <span className={styles.unidade}>/ {produto.unidade_medida}</span>
        </p>
      ) : (
        <p className={styles.preco}>
          {formatarPreco(produto.preco_unitario)} <span className={styles.unidade}>/ {produto.unidade_medida}</span>
        </p>
      )}
      <button
        className={styles.botao}
        onClick={() => onAdicionar(produto)}
        disabled={semEstoque}
      >
        {semEstoque ? "Sem estoque" : "Adicionar ao carrinho"}
      </button>
    </div>
  );
}
