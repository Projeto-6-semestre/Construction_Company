"use client";

import { useEffect, useState } from "react";
import { ApiError, getProdutos } from "@/lib/api";
import type { Produto } from "@/types/api";
import styles from "./StockSidebar.module.css";

// A API devolve "300.000" (3 casas decimais fixas da coluna do banco) - exibir
// isso cru confundiria quem le em pt-BR (ponto = separador de milhar nesse
// idioma). Number() descarta os zeros extras, toLocaleString formata direito
// (5000 vira "5.000" de verdade, 300 continua "300").
function formatarQuantidade(valor: string): string {
  return Number(valor).toLocaleString("pt-BR", { maximumFractionDigits: 3 });
}

export function StockSidebar() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [recarregarToken, setRecarregarToken] = useState(0);

  useEffect(() => {
    let ignorar = false;

    setCarregando(true);
    setErro(null);

    getProdutos()
      .then((dados) => {
        if (!ignorar) setProdutos(dados);
      })
      .catch((e) => {
        if (!ignorar) {
          setErro(e instanceof ApiError ? e.message : "Erro inesperado ao carregar o estoque.");
        }
      })
      .finally(() => {
        if (!ignorar) setCarregando(false);
      });

    return () => {
      ignorar = true;
    };
  }, [recarregarToken]);

  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <h2>Estoque atual</h2>
        <button
          className={styles.refreshButton}
          onClick={() => setRecarregarToken((t) => t + 1)}
          disabled={carregando}
        >
          {carregando ? "Atualizando..." : "Atualizar"}
        </button>
      </div>

      {erro && <p className={styles.erro}>{erro}</p>}

      {!erro && produtos.length === 0 && !carregando && (
        <p className={styles.vazio}>Nenhum produto cadastrado ainda.</p>
      )}

      <div className={styles.tabelaScroll}>
        <table className={styles.tabela}>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Produto</th>
              <th>Qtd.</th>
            </tr>
          </thead>
          <tbody>
            {produtos.map((p) => {
              const abaixoDoMinimo = Number(p.quantidade_atual) < Number(p.quantidade_minima);
              return (
                <tr key={p.id} className={abaixoDoMinimo ? styles.linhaAlerta : undefined}>
                  <td className={styles.sku}>{p.sku}</td>
                  <td>{p.nome}</td>
                  <td className={styles.quantidade}>
                    {formatarQuantidade(p.quantidade_atual)} {p.unidade_medida}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </aside>
  );
}
