export interface Produto {
  id: number;
  sku: string;
  nome: string;
  categoria: string;
  unidade_medida: string;
  quantidade_atual: string;
  quantidade_minima: string;
  preco_unitario: string;
  preco_promocional: string | null;
  imagem_url: string | null;
  criado_em: string;
  atualizado_em: string;
}

export interface ProdutoPage {
  items: Produto[];
  total: number;
  page: number;
  page_size: number;
}

export interface ProdutoCreateInput {
  sku: string;
  nome: string;
  categoria: string;
  unidade_medida: string;
  quantidade_atual: number;
  quantidade_minima: number;
  preco_unitario: number;
  preco_promocional?: number | null;
  imagem_url?: string | null;
}

export interface ProdutoUpdateInput {
  nome?: string;
  categoria?: string;
  unidade_medida?: string;
  quantidade_minima?: number;
  preco_unitario?: number;
  preco_promocional?: number | null;
  imagem_url?: string | null;
}

export interface ItemPedidoInput {
  sku: string;
  quantidade: number;
}

export interface PedidoResponse {
  id: number;
  cliente_nome: string;
  status: string;
  criado_em: string;
  itens: { id: number; produto_id: number; quantidade: string }[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  pergunta: string;
  historico: ChatMessage[];
}

export interface ChatResponse {
  resposta: string;
}
