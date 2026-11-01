import { getToken } from "@/lib/auth";
import type {
  ChatMessage,
  ChatResponse,
  ItemPedidoInput,
  PedidoResponse,
  Produto,
  ProdutoCreateInput,
  ProdutoPage,
  ProdutoUpdateInput,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(username: string, senha: string): Promise<string> {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, senha }),
  });
  if (!res.ok) {
    throw new ApiError("Usuário ou senha incorretos.", res.status);
  }
  const dados = await res.json();
  return dados.access_token as string;
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
    headers: authHeaders(),
  });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar o estoque.", res.status);
  }
  return res.json();
}

export async function criarProduto(dados: ProdutoCreateInput): Promise<Produto> {
  const res = await fetch(`${API_BASE_URL}/produtos`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(dados),
  });
  if (!res.ok) {
    const corpo = await res.json().catch(() => null);
    const mensagem = res.status === 409 ? "Já existe um produto com esse SKU." : "Não foi possível criar o produto.";
    throw new ApiError(mensagem, res.status, corpo);
  }
  return res.json();
}

export async function atualizarProduto(id: number, dados: ProdutoUpdateInput): Promise<Produto> {
  const res = await fetch(`${API_BASE_URL}/produtos/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(dados),
  });
  if (!res.ok) {
    throw new ApiError("Não foi possível atualizar o produto.", res.status);
  }
  return res.json();
}

export async function getCategorias(): Promise<string[]> {
  const res = await fetch(`${API_BASE_URL}/produtos/categorias`, { cache: "no-store" });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar as categorias.", res.status);
  }
  return res.json();
}

export async function getCatalogo(params: {
  categoria?: string;
  page?: number;
  pageSize?: number;
}): Promise<ProdutoPage> {
  const query = new URLSearchParams();
  if (params.categoria) query.set("categoria", params.categoria);
  query.set("page", String(params.page ?? 1));
  query.set("page_size", String(params.pageSize ?? 12));

  const res = await fetch(`${API_BASE_URL}/produtos/catalogo?${query.toString()}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar o catalogo.", res.status);
  }
  return res.json();
}

export async function postPedido(
  clienteNome: string,
  itens: ItemPedidoInput[],
): Promise<PedidoResponse> {
  const res = await fetch(`${API_BASE_URL}/pedidos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cliente_nome: clienteNome, itens }),
  });
  if (!res.ok) {
    const corpo = await res.json().catch(() => null);
    const mensagem =
      res.status === 409
        ? "Estoque insuficiente para um ou mais itens do carrinho."
        : "Nao foi possivel finalizar o pedido.";
    throw new ApiError(mensagem, res.status, corpo);
  }
  return res.json();
}

export async function postChat(pergunta: string, historico: ChatMessage[]): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ pergunta, historico }),
  });
  if (!res.ok) {
    throw new ApiError("O agente nao conseguiu responder agora.", res.status);
  }
  return res.json();
}
