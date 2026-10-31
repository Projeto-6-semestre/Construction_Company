import type { ChatMessage, ChatResponse, Produto } from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function getProdutos(params?: {
  categoria?: string;
  abaixoDoMinimo?: boolean;
}): Promise<Produto[]> {
  const query = new URLSearchParams();
  if (params?.categoria) query.set("categoria", params.categoria);
  if (params?.abaixoDoMinimo) query.set("abaixo_do_minimo", "true");

  const res = await fetch(`${API_BASE_URL}/produtos?${query.toString()}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar o estoque.", res.status);
  }
  return res.json();
}

export async function postChat(pergunta: string, historico: ChatMessage[]): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pergunta, historico }),
  });
  if (!res.ok) {
    throw new ApiError("O agente nao conseguiu responder agora.", res.status);
  }
  return res.json();
}
