import styles from "./SobreContato.module.css";

const DESTAQUES = [
  {
    icone: "📦",
    titulo: "Estoque em tempo real",
    texto: "A quantidade que você vê aqui é a mesma do nosso sistema interno — sem planilha desatualizada.",
  },
  {
    icone: "🛒",
    titulo: "Peça direto pelo site",
    texto: "Monte o carrinho, finalize o pedido e a gente já separa o material pra você.",
  },
  {
    icone: "🤖",
    titulo: "Atendimento com IA",
    texto: "Nosso agente inteligente ajuda a consultar estoque e tirar dúvidas rapidinho, a qualquer hora.",
  },
];

// Secao institucional no rodape da loja (quem somos + contato). Conteudo
// estatico, so os dados de contato sao placeholder (ver aviso no final da secao).
export function SobreContato() {
  return (
    <section className={styles.secao}>
      <div className={styles.grid}>
        <div className={styles.sobre}>
          <h2>Quem Somos</h2>
          <p>
            A Construction Company existe pra resolver um problema simples: comprar material
            de construção sem precisar ligar pra saber se tem estoque. Nosso catálogo é
            atualizado em tempo real, direto do nosso sistema de controle de estoque — o que
            você vê aqui é exatamente o que temos disponível.
          </p>

          <div className={styles.destaques}>
            {DESTAQUES.map((d) => (
              <div key={d.titulo} className={styles.destaque}>
                <span className={styles.destaqueIcone}>{d.icone}</span>
                <div>
                  <h3>{d.titulo}</h3>
                  <p>{d.texto}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.contato}>
          <h2>Fale Conosco</h2>
          <p className={styles.contatoIntro}>Dúvidas sobre produtos, pedidos ou entrega:</p>
          <ul className={styles.contatoLista}>
            <li>
              <span className={styles.contatoIcone}>✉️</span> contato@construction-company.com.br
            </li>
            <li>
              <span className={styles.contatoIcone}>📞</span> (11) 0000-0000
            </li>
            <li>
              <span className={styles.contatoIcone}>📍</span> São Paulo — SP
            </li>
          </ul>
          <p className={styles.aviso}>* dados de contato de exemplo — atualizar com as informações reais</p>
        </div>
      </div>
    </section>
  );
}
