"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ApiError, login } from "@/lib/api";
import { setToken } from "@/lib/auth";
import styles from "./page.module.css";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function entrar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      const token = await login(username.trim(), senha);
      setToken(token);
      router.push("/");
    } catch (e) {
      setErro(e instanceof ApiError ? e.message : "Erro inesperado ao entrar.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main className={styles.main}>
      <form className={styles.card} onSubmit={entrar}>
        <h1>Painel interno</h1>
        <p className={styles.subtitulo}>Acesso restrito à equipe — materiais de construção.</p>

        <label className={styles.campo}>
          <span>Usuário</span>
          <input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoFocus
            required
          />
        </label>

        <label className={styles.campo}>
          <span>Senha</span>
          <input
            id="senha"
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
        </label>

        {erro && <p className={styles.erro}>{erro}</p>}

        <button type="submit" className={styles.botao} disabled={enviando}>
          {enviando ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </main>
  );
}
