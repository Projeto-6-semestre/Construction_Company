"use client";

import { useState } from "react";
import { ApiError, postPedido } from "@/lib/api";
import type { Produto } from "@/types/api";
import styles from "./CartDrawer.module.css";

export interface ItemCarrinho {
  produto: Produto;
  quantidade: number;
}

interface Props {
  aberto: boolean;
  itens: ItemCarrinho[];
  onFechar: () => void;
  onAlterarQuantidade: (sku: string, quantidade: number) => void;
  onRemover: (sku: string) => void;
  onPedidoConfirmado: () => void;
}

function formatarPreco(valor: number): string {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function precoEfetivo(produto: Produto): number {
  return produto.preco_promocional !== null
    ? Number(produto.preco_promocional)
    : Number(produto.preco_unitario);
}

export function CartDrawer({
  aberto,
  itens,
  onFechar,
  onAlterarQuantidade,
  onRemover,
  onPedidoConfirmado,
}: Props) {
  const [clienteNome, setClienteNome] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [numeroPedido, setNumeroPedido] = useState<number | null>(null);

  const total = itens.reduce((soma, item) => soma + precoEfetivo(item.produto) * item.quantidade, 0);

  async function finalizar() {
    if (!clienteNome.trim() || itens.length === 0) return;
    setEnviando(true);
    setErro(null);
    try {
      const pedido = await postPedido(
        clienteNome.trim(),
        itens.map((item) => ({ sku: item.produto.sku, quantidade: item.quantidade })),
      );
      setNumeroPedido(pedido.id);
      onPedidoConfirmado();
    } catch (e) {
      setErro(e instanceof ApiError ? e.message : "Erro inesperado ao finalizar o pedido.");
    } finally {
      setEnviando(false);
    }
  }

  if (!aberto) return null;

  return (
    <div className={styles.overlay} onClick={onFechar}>
      <aside className={styles.painel} onClick={(e) => e.stopPropagation()}>
        <div className={styles.cabecalho}>
          <h2>Seu carrinho</h2>
          <button className={styles.fechar} onClick={onFechar} aria-label="Fechar carrinho">
            ×
          </button>
        </div>

        {numeroPedido !== null ? (
          <div className={styles.sucesso}>
            <p>✅ Pedido #{numeroPedido} confirmado!</p>
            <p className={styles.sucessoDetalhe}>A equipe já foi notificada e vai separar seu material.</p>
            <button className={styles.botaoPrimario} onClick={onFechar}>
              Fechar
            </button>
          </div>
        ) : (
          <>
            {itens.length === 0 ? (
              <p className={styles.vazio}>Seu carrinho está vazio.</p>
            ) : (
              <div className={styles.lista}>
                {itens.map((item) => (
                  <div key={item.produto.sku} className={styles.item}>
                    <div className={styles.itemInfo}>
                      <p className={styles.itemNome}>{item.produto.nome}</p>
                      <p className={styles.itemPreco}>
                        {formatarPreco(precoEfetivo(item.produto))} / {item.produto.unidade_medida}
                      </p>
                    </div>
                    <div className={styles.itemControles}>
                      <input
                        type="number"
                        min={1}
                        value={item.quantidade}
                        onChange={(e) =>
                          onAlterarQuantidade(item.produto.sku, Number(e.target.value) || 1)
                        }
                        className={styles.inputQtd}
                      />
                      <button
                        className={styles.removerBtn}
                        onClick={() => onRemover(item.produto.sku)}
                        aria-label={`Remover ${item.produto.nome}`}
                      >
                        Remover
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className={styles.rodape}>
              <p className={styles.total}>Total: {formatarPreco(total)}</p>
              <input
                className={styles.inputNome}
                placeholder="Seu nome completo"
                value={clienteNome}
                onChange={(e) => setClienteNome(e.target.value)}
                disabled={itens.length === 0}
              />
              {erro && <p className={styles.erro}>{erro}</p>}
              <button
                className={styles.botaoPrimario}
                onClick={finalizar}
                disabled={enviando || itens.length === 0 || !clienteNome.trim()}
              >
                {enviando ? "Enviando..." : "Finalizar pedido"}
              </button>
            </div>
          </>
        )}
      </aside>
    </div>
  );
}
