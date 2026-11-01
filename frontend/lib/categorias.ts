// Mapa so de apresentacao (icone + rotulo) pra cada categoria REAL do catalogo
// (a lista de categorias em si vem da API, nunca hardcoded aqui). Categoria sem
// mapeamento cai no fallback generico - nao quebra se um produto novo vier com
// categoria ainda nao mapeada.
const ICONES: Record<string, string> = {
  bloco: "🧱",
  cimento: "🏗️",
  areia: "🏖️",
  brita: "🪨",
  ferragem: "🔩",
  ferramenta: "🧰",
  hidraulica: "🚰",
  telha: "🏠",
  tinta: "🎨",
};

const ROTULOS: Record<string, string> = {
  bloco: "Blocos e Tijolos",
  cimento: "Cimento e Argamassa",
  areia: "Areia e Agregados",
  brita: "Brita",
  ferragem: "Ferragens",
  ferramenta: "Ferramentas",
  hidraulica: "Hidráulica",
  telha: "Telhas",
  tinta: "Tintas",
};

export function iconeCategoria(categoria: string): string {
  return ICONES[categoria] ?? "📦";
}

export function rotuloCategoria(categoria: string): string {
  return ROTULOS[categoria] ?? categoria.charAt(0).toUpperCase() + categoria.slice(1);
}
