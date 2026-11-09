"use client";

import { useState } from "react";
import { ApiError, postPedido } from "@/lib/api";
import { WHATSAPP_NUMERO } from "@/lib/contato";
import type { Produto } from "@/types/api";
import styles from "./CartDrawer.module.css";

// Um item dentro do carrinho (estado vive na pagina da loja, CartDrawer so exibe/edita).
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

// Preco que realmente vale pro produto: promocional se existir, senao o normal.
function precoEfetivo(produto: Produto): number {
  return produto.preco_promocional !== null
    ? Number(produto.preco_promocional)
    : Number(produto.preco_unitario);
}

// Painel lateral (drawer) do carrinho: lista os itens, deixa editar quantidade
// e finaliza o pedido chamando a API.
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

  // Monta a mensagem do pedido pro WhatsApp da empresa - mesma logica de site
  // de pizzaria: o pedido ja fica salvo no banco (pro painel interno ver),
  // e o cliente manda esse resumo pra combinar pagamento/entrega.
  function montarMensagemWhatsapp(pedidoId: number): string {
    const linhas = itens.map(
      (item) =>
        `- ${item.quantidade}x ${item.produto.nome} (${formatarPreco(precoEfetivo(item.produto))}/${item.produto.unidade_medida})`,
    );
    return [
      `Olá! Gostaria de confirmar meu pedido #${pedidoId}:`,
      "",
      ...linhas,
      "",
      `Total: ${formatarPreco(total)}`,
      "",
      `Nome: ${clienteNome.trim()}`,
    ].join("\n");
  }

  // Envia o pedido pra API. Se der 409 (estoque insuficiente), a mensagem de
  // erro da API ja vem pronta pra mostrar - ver postPedido em lib/api.ts.
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
      // Abre o WhatsApp numa aba nova com o pedido ja escrito - o cliente so
      // confere e aperta enviar. Nao bloqueia a tela de sucesso se o navegador
      // bloquear o popup, o pedido ja foi salvo de qualquer forma.
      const url = `https://wa.me/${WHATSAPP_NUMERO}?text=${encodeURIComponent(montarMensagemWhatsapp(pedido.id))}`;
      window.open(url, "_blank", "noopener,noreferrer");
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
            <p className={styles.sucessoDetalhe}>
              Abrimos o WhatsApp numa aba nova com o resumo do pedido — é só conferir e enviar pra
              gente combinar pagamento e entrega. Se não abriu, seu navegador pode ter bloqueado o
              pop-up.
            </p>
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
              {!clienteNome.trim() && itens.length > 0 && (
                <p className={styles.dica}>Preencha seu nome acima pra liberar o botão.</p>
              )}
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
