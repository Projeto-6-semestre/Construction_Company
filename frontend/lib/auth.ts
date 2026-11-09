// Guarda/le/apaga o token JWT do login do painel interno no localStorage do navegador.
const CHAVE_TOKEN = "painel_token";

// localStorage e simples o suficiente pro prazo deste projeto, mas vale saber
// a troca: um token em localStorage e acessivel por qualquer script na pagina
// (risco de XSS). O jeito mais robusto (cookie httpOnly + middleware do
// Next.js) fica como proxima melhoria, nao foi feito aqui por tempo.
export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem(CHAVE_TOKEN);
  } catch {
    return null;
  }
}

export function setToken(token: string): void {
  try {
    window.localStorage.setItem(CHAVE_TOKEN, token);
  } catch {
    // localStorage indisponivel (modo privado etc.) - segue sem persistir
  }
}

export function limparToken(): void {
  try {
    window.localStorage.removeItem(CHAVE_TOKEN);
  } catch {
    // ignora
  }
}
