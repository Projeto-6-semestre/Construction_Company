"use client";

import { useRef, useState } from "react";
import { ApiError, postChat } from "@/lib/api";
import type { ChatMessage } from "@/types/api";
import { ChatMessageBubble } from "./ChatMessageBubble";
import styles from "./ChatPanel.module.css";

const SUGESTOES = [
  "Qual o estoque de cimento?",
  "Quais produtos estao abaixo do minimo?",
  "Registrar pedido de 100 blocos BLOCO-09 pro cliente Joao",
];

// Painel de chat com o agente de IA (painel interno). Guarda o historico da
// conversa em memoria (perde ao recarregar a pagina - sem persistencia).
export function ChatPanel() {
  const [mensagens, setMensagens] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Oi! Sou o agente de estoque. Posso consultar o que tem disponivel, registrar pedidos de cliente ou dar entrada de mercadoria de fornecedor. O que voce precisa?",
    },
  ]);
  const [pergunta, setPergunta] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const listRef = useRef<HTMLDivElement>(null);

  // Envia a pergunta pro back-end junto com o historico (pra IA ter contexto da
  // conversa) e adiciona a resposta na lista. Usado tanto pelo input quanto pelos
  // botoes de sugestao.
  async function enviar(texto: string) {
    const textoLimpo = texto.trim();
    if (!textoLimpo || enviando) return;

    const historico = mensagens;
    const novaMensagemUsuario: ChatMessage = { role: "user", content: textoLimpo };
    setMensagens((atual) => [...atual, novaMensagemUsuario]);
    setPergunta("");
    setErro(null);
    setEnviando(true);

    try {
      const resposta = await postChat(textoLimpo, historico);
      setMensagens((atual) => [...atual, { role: "assistant", content: resposta.resposta }]);
    } catch (e) {
      setErro(e instanceof ApiError ? e.message : "Erro inesperado ao falar com o agente.");
    } finally {
      setEnviando(false);
      requestAnimationFrame(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
      });
    }
  }

  return (
    <section className={styles.panel}>
      <div ref={listRef} className={styles.lista}>
        {mensagens.map((m, i) => (
          <ChatMessageBubble key={i} message={m} />
        ))}
        {enviando && <p className={styles.digitando}>Consultando o estoque...</p>}
        {erro && <p className={styles.erro}>{erro}</p>}
      </div>

      <div className={styles.sugestoes}>
        {SUGESTOES.map((s) => (
          <button key={s} className={styles.sugestao} onClick={() => enviar(s)} disabled={enviando}>
            {s}
          </button>
        ))}
      </div>

      <form
        className={styles.formulario}
        onSubmit={(e) => {
          e.preventDefault();
          enviar(pergunta);
        }}
      >
        <input
          id="chat-input"
          className={styles.input}
          value={pergunta}
          onChange={(e) => setPergunta(e.target.value)}
          placeholder="Pergunte sobre o estoque..."
          disabled={enviando}
        />
        <button type="submit" className={styles.enviarButton} disabled={enviando || !pergunta.trim()}>
          Enviar
        </button>
      </form>
    </section>
  );
}
