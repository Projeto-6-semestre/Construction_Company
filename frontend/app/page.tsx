import { ChatPanel } from "@/components/ChatPanel";
import { StockSidebar } from "@/components/StockSidebar";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1>Agente de Estoque</h1>
        <p>Materiais de construcao - pergunte sobre o estoque ou registre pedidos pelo chat.</p>
      </header>
      <div className={styles.conteudo}>
        <StockSidebar />
        <ChatPanel />
      </div>
    </main>
  );
}
