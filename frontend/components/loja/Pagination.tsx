"use client";

import styles from "./Pagination.module.css";

interface Props {
  paginaAtual: number;
  totalPaginas: number;
  onMudarPagina: (pagina: number) => void;
}

// Navegacao de paginas do catalogo (numeros + setas). Some sozinha se so
// existir 1 pagina de resultado.
export function Pagination({ paginaAtual, totalPaginas, onMudarPagina }: Props) {
  if (totalPaginas <= 1) return null;

  const paginas = Array.from({ length: totalPaginas }, (_, i) => i + 1);

  return (
    <nav className={styles.nav} aria-label="Paginação de produtos">
      <button
        className={styles.seta}
        onClick={() => onMudarPagina(paginaAtual - 1)}
        disabled={paginaAtual <= 1}
        aria-label="Página anterior"
      >
        ‹
      </button>
      {paginas.map((pagina) => (
        <button
          key={pagina}
          className={`${styles.pagina} ${pagina === paginaAtual ? styles.paginaAtiva : ""}`}
          onClick={() => onMudarPagina(pagina)}
          aria-current={pagina === paginaAtual ? "page" : undefined}
        >
          {pagina}
        </button>
      ))}
      <button
        className={styles.seta}
        onClick={() => onMudarPagina(paginaAtual + 1)}
        disabled={paginaAtual >= totalPaginas}
        aria-label="Próxima página"
      >
        ›
      </button>
    </nav>
  );
}
