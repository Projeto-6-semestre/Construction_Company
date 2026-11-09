// Tipos que espelham os schemas Pydantic do back-end (app/models/schemas.py).
// Se um campo mudar la, precisa atualizar aqui tambem - nao ha geracao automatica.
//
// Nota: campos numericos (quantidade, preco) chegam como STRING ("12.500"), nao
// como number - o back-end usa Decimal/Numeric pra nao perder precisao em dinheiro
// e quantidade, e o JSON representa isso como string pra nao arredondar errado.
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

// Resposta paginada do catalogo: os produtos da pagina atual + total geral (pra
// calcular quantas paginas existem).
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

// Um item do carrinho ao enviar o pedido - so SKU e quantidade, o back-end
// busca o resto (nome, preco) no banco pra nao confiar em dado vindo do navegador.
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

// Uma mensagem do historico do chat - "user" = o que a pessoa digitou,
// "assistant" = o que o agente de IA respondeu.
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
