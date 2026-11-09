"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { RequireAuth } from "@/components/RequireAuth";
import { ApiError, getPedidos } from "@/lib/api";
import type { PedidoResponse } from "@/types/api";
import styles from "./page.module.css";

// pt-BR, dia/mes/ano hora:minuto - mais facil de ler que o ISO cru que a API manda.
function formatarData(iso: string): string {
  return new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Tela do painel interno pra equipe ver os pedidos feitos na loja publica -
// nao mostra preco/total porque o pedido nao guarda um "preco na hora da
// compra" (so a quantidade por item), so nome do cliente e o que foi pedido.
function PainelPedidos() {
  const [pedidos, setPedidos] = useState<PedidoResponse[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    getPedidos()
      .then(setPedidos)
      .catch((e) => setErro(e instanceof ApiError ? e.message : "Erro ao carregar pedidos."))
      .finally(() => setCarregando(false));
  }, []);

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <div>
          <h1>Pedidos</h1>
          <p>Pedidos feitos pelos clientes na loja pública, mais recentes primeiro.</p>
        </div>
        <Link href="/" className={styles.link}>
          ← Voltar ao painel
        </Link>
      </header>

      {erro && <p className={styles.erro}>{erro}</p>}

      {carregando ? (
        <p className={styles.estado}>Carregando...</p>
      ) : pedidos.length === 0 ? (
        <p className={styles.estado}>Nenhum pedido ainda.</p>
      ) : (
        <div className={styles.lista}>
          {pedidos.map((pedido) => (
            <article key={pedido.id} className={styles.cartao}>
              <div className={styles.cartaoCabecalho}>
                <div>
                  <span className={styles.numeroPedido}>Pedido #{pedido.id}</span>
                  <span className={styles.status}>{pedido.status}</span>
                </div>
                <span className={styles.data}>{formatarData(pedido.criado_em)}</span>
              </div>
              <p className={styles.cliente}>{pedido.cliente_nome}</p>
              <ul className={styles.itens}>
                {pedido.itens.map((item) => (
                  <li key={item.id}>
                    {item.quantidade}x {item.produto.nome}{" "}
                    <span className={styles.sku}>({item.produto.sku})</span>
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}

export default function PedidosPage() {
  return (
    <RequireAuth>
      <PainelPedidos />
    </RequireAuth>
  );
}
