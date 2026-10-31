export interface Produto {
  id: number;
  sku: string;
  nome: string;
  categoria: string;
  unidade_medida: string;
  quantidade_atual: string;
  quantidade_minima: string;
  preco_unitario: string;
  criado_em: string;
  atualizado_em: string;
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
