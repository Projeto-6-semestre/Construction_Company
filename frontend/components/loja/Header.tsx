"use client";

import Image from "next/image";
import Link from "next/link";
import styles from "./Header.module.css";

interface Props {
  quantidadeCarrinho: number;
  onAbrirCarrinho: () => void;
}

export function Header({ quantidadeCarrinho, onAbrirCarrinho }: Props) {
  return (
    <header className={styles.header}>
      <div className={styles.conteudo}>
        <Link href="/loja" className={styles.marca}>
          <Image
            src="/images/logo.png"
            alt="Construction Company"
            width={44}
            height={44}
            className={styles.logoImg}
          />
          <div className={styles.marcaTexto}>
            <span className={styles.marcaNome}>Construction Company</span>
            <span className={styles.marcaSlogan}>Materiais de Construção</span>
          </div>
        </Link>

        <nav className={styles.nav}>
          <Link href="/loja" className={styles.navLink}>
            Loja
          </Link>
          <Link href="/" className={styles.navLink}>
            Painel interno
          </Link>
          <button className={styles.botaoCarrinho} onClick={onAbrirCarrinho}>
            🛒 <span>Carrinho{quantidadeCarrinho > 0 ? ` (${quantidadeCarrinho})` : ""}</span>
          </button>
        </nav>
      </div>
    </header>
  );
}
