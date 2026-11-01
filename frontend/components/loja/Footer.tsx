import Image from "next/image";
import Link from "next/link";
import { rotuloCategoria } from "@/lib/categorias";
import styles from "./Footer.module.css";

const CATEGORIAS_DESTAQUE = ["bloco", "cimento", "areia", "ferramenta"];
const ANO_ATUAL = new Date().getFullYear();

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.grid}>
        <div className={styles.colunaMarca}>
          <div className={styles.marca}>
            <Image src="/images/logo.png" alt="" width={36} height={36} className={styles.logo} />
            <span className={styles.marcaNome}>Construction Company</span>
          </div>
          <p className={styles.descricao}>
            Materiais de construção para sua obra, da areia ao acabamento — estoque
            atualizado em tempo real, pedido feito online.
          </p>
        </div>

        <div className={styles.coluna}>
          <h4>Categorias</h4>
          <ul>
            {CATEGORIAS_DESTAQUE.map((categoria) => (
              <li key={categoria}>
                <Link href={`/loja?categoria=${categoria}`}>{rotuloCategoria(categoria)}</Link>
              </li>
            ))}
            <li>
              <Link href="/loja">Ver catálogo completo</Link>
            </li>
          </ul>
        </div>

        <div className={styles.coluna}>
          <h4>Empresa</h4>
          <ul>
            <li>
              <Link href="/">Painel interno</Link>
            </li>
            <li>
              <a href="https://github.com/Projeto-6-semestre/Construction_Company" target="_blank" rel="noopener noreferrer">
                Projeto no GitHub
              </a>
            </li>
          </ul>
        </div>

        <div className={styles.coluna}>
          <h4>Contato</h4>
          <ul className={styles.listaPlaceholder}>
            <li>contato@construction-company.com.br</li>
            <li>(11) 0000-0000</li>
            <li className={styles.aviso}>* dados de exemplo — atualizar com o contato real</li>
          </ul>
        </div>
      </div>

      <div className={styles.rodapeInferior}>
        <span>
          © {ANO_ATUAL} Construction Company. Todos os direitos reservados.
        </span>
        <span>São Paulo — SP</span>
      </div>
    </footer>
  );
}
