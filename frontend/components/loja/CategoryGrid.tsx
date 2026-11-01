"use client";

import { iconeCategoria, rotuloCategoria } from "@/lib/categorias";
import styles from "./CategoryGrid.module.css";

interface Props {
  categorias: string[];
  categoriaAtiva: string | null;
  onSelecionar: (categoria: string | null) => void;
}

export function CategoryGrid({ categorias, categoriaAtiva, onSelecionar }: Props) {
  return (
    <section className={styles.secao}>
      <h2 className={styles.titulo}>Quais tipos de materiais você deseja</h2>
      <div className={styles.grid}>
        <button
          className={`${styles.card} ${categoriaAtiva === null ? styles.cardAtivo : ""}`}
          onClick={() => onSelecionar(null)}
        >
          <span className={styles.icone}>🗂️</span>
          <span className={styles.rotulo}>Todos</span>
        </button>
        {categorias.map((categoria) => (
          <button
            key={categoria}
            className={`${styles.card} ${categoriaAtiva === categoria ? styles.cardAtivo : ""}`}
            onClick={() => onSelecionar(categoria)}
          >
            <span className={styles.icone}>{iconeCategoria(categoria)}</span>
            <span className={styles.rotulo}>{rotuloCategoria(categoria)}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
