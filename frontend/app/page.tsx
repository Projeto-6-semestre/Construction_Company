"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { ChatPanel } from "@/components/ChatPanel";
import { RequireAuth } from "@/components/RequireAuth";
import { StockSidebar } from "@/components/StockSidebar";
import { limparToken } from "@/lib/auth";
import styles from "./page.module.css";

function PainelInterno() {
  const router = useRouter();

  function sair() {
    limparToken();
    router.push("/login");
  }

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <div>
          <h1>Agente de Estoque</h1>
          <p>Materiais de construcao - pergunte sobre o estoque ou registre pedidos pelo chat.</p>
        </div>
        <nav className={styles.navHeader}>
          <Link href="/produtos" className={styles.linkLoja}>
            Gerenciar produtos
          </Link>
          <Link href="/loja" className={styles.linkLoja}>
            Ver loja →
          </Link>
          <button className={styles.botaoSair} onClick={sair}>
            Sair
          </button>
        </nav>
      </header>
      <div className={styles.conteudo}>
        <StockSidebar />
        <ChatPanel />
      </div>
    </main>
  );
}

export default function Home() {
  return (
    <RequireAuth>
      <PainelInterno />
    </RequireAuth>
  );
}
