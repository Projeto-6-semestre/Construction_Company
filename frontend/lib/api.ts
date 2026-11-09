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

// Todas as funcoes deste arquivo chamam a API do back-end (FastAPI, em Python).
// E a UNICA camada do front-end que fala HTTP com o back-end - telas e componentes
// nunca fazem fetch direto, sempre passam por aqui.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

// Erro customizado lancado quando a API responde com status de erro (4xx/5xx).
// Guarda o status HTTP e o corpo da resposta pra quem chamou decidir como tratar.
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

// Monta o cabecalho "Authorization: Bearer <token>" pras rotas que exigem login
// (painel interno). Se nao tiver token salvo, manda sem header - a API que recusa.
function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Login do painel interno: manda usuario/senha, recebe o token JWT de volta.
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

// Lista de produtos pro painel interno (exige login). Pode filtrar por categoria
// ou so os que estao abaixo da quantidade minima (alerta de reposicao).
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

// Cadastra um produto novo no estoque (painel interno). Erro 409 = SKU repetido.
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

// Edita um produto existente (painel interno) - so manda os campos que mudaram.
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

// Lista as categorias que existem de verdade no catalogo (usado nos filtros da loja
// publica). Nao exige login - rota publica.
export async function getCategorias(): Promise<string[]> {
  const res = await fetch(`${API_BASE_URL}/produtos/categorias`, { cache: "no-store" });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar as categorias.", res.status);
  }
  return res.json();
}

// Catalogo paginado da loja publica (sem exigir login). Usado na pagina /loja
// pra listar os produtos com filtro de categoria e paginacao.
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

// Finaliza um pedido da loja publica (conteudo do carrinho). Erro 409 = algum
// item do carrinho nao tem estoque suficiente - o back-end valida tudo antes de
// gravar qualquer coisa, entao ou o pedido inteiro entra, ou nada entra.
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

// Lista os pedidos feitos na loja, mais recentes primeiro (painel interno,
// exige login) - pra equipe acompanhar o que os clientes compraram.
export async function getPedidos(): Promise<PedidoResponse[]> {
  const res = await fetch(`${API_BASE_URL}/pedidos`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) {
    throw new ApiError("Nao foi possivel carregar os pedidos.", res.status);
  }
  return res.json();
}

// Manda a pergunta do usuario (+ historico da conversa) pro agente de IA no
// back-end e recebe a resposta em texto. Usado no chat do painel interno.
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
