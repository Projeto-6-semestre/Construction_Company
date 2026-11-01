"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { CartDrawer, type ItemCarrinho } from "@/components/loja/CartDrawer";
import { CategoryGrid } from "@/components/loja/CategoryGrid";
import { Footer } from "@/components/loja/Footer";
import { Header } from "@/components/loja/Header";
import { Pagination } from "@/components/loja/Pagination";
import { ProductCard } from "@/components/loja/ProductCard";
import { SobreContato } from "@/components/loja/SobreContato";
import { ApiError, getCatalogo, getCategorias } from "@/lib/api";
import { rotuloCategoria } from "@/lib/categorias";
import type { Produto } from "@/types/api";
import styles from "./page.module.css";

const TAMANHO_PAGINA = 8;

function LojaConteudo() {
  const searchParams = useSearchParams();
  const [categorias, setCategorias] = useState<string[]>([]);
  const [categoriaAtiva, setCategoriaAtiva] = useState<string | null>(
    () => searchParams.get("categoria"),
  );
  const [pagina, setPagina] = useState(1);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [total, setTotal] = useState(0);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [carrinhoAberto, setCarrinhoAberto] = useState(false);
  const [itensCarrinho, setItensCarrinho] = useState<ItemCarrinho[]>([]);

  useEffect(() => {
    getCategorias()
      .then(setCategorias)
      .catch(() => {});
  }, []);

  useEffect(() => {
    let ignorar = false;
    setCarregando(true);
    setErro(null);

    getCatalogo({ categoria: categoriaAtiva ?? undefined, page: pagina, pageSize: TAMANHO_PAGINA })
      .then((resultado) => {
        if (ignorar) return;
        setProdutos(resultado.items);
        setTotal(resultado.total);
      })
      .catch((e) => {
        if (!ignorar) {
          setErro(e instanceof ApiError ? e.message : "Erro inesperado ao carregar o catálogo.");
        }
      })
      .finally(() => {
        if (!ignorar) setCarregando(false);
      });

    return () => {
      ignorar = true;
    };
  }, [categoriaAtiva, pagina]);

  function selecionarCategoria(categoria: string | null) {
    setCategoriaAtiva(categoria);
    setPagina(1);
  }

  function adicionarAoCarrinho(produto: Produto) {
    setItensCarrinho((atual) => {
      const existente = atual.find((item) => item.produto.sku === produto.sku);
      if (existente) {
        return atual.map((item) =>
          item.produto.sku === produto.sku ? { ...item, quantidade: item.quantidade + 1 } : item,
        );
      }
      return [...atual, { produto, quantidade: 1 }];
    });
    setCarrinhoAberto(true);
  }

  function alterarQuantidade(sku: string, quantidade: number) {
    setItensCarrinho((atual) =>
      atual.map((item) => (item.produto.sku === sku ? { ...item, quantidade } : item)),
    );
  }

  function removerDoCarrinho(sku: string) {
    setItensCarrinho((atual) => atual.filter((item) => item.produto.sku !== sku));
  }

  const totalPaginas = Math.max(1, Math.ceil(total / TAMANHO_PAGINA));
  const quantidadeNoCarrinho = itensCarrinho.reduce((soma, item) => soma + item.quantidade, 0);

  return (
    <div className={styles.pagina}>
      <Header quantidadeCarrinho={quantidadeNoCarrinho} onAbrirCarrinho={() => setCarrinhoAberto(true)} />

      <main className={styles.main}>
        <nav className={styles.migalha} aria-label="Navegação">
          <span>Home</span>
          <span className={styles.separador}>›</span>
          <span>{categoriaAtiva ? rotuloCategoria(categoriaAtiva) : "Materiais de Construção"}</span>
        </nav>

        <header className={styles.cabecalhoPagina}>
          <h1>Materiais de Construção</h1>
          <p>
            Há diversos tipos de material de construção com finalidades e propostas diferentes.
            Escolha a categoria ou filtre pelo catálogo abaixo.
          </p>
        </header>

        <CategoryGrid
          categorias={categorias}
          categoriaAtiva={categoriaAtiva}
          onSelecionar={selecionarCategoria}
        />

        <section className={styles.secaoProdutos}>
          <h2 className={styles.tituloProdutos}>
            {categoriaAtiva ? rotuloCategoria(categoriaAtiva) : "Todos os produtos"}
            {!carregando && <span className={styles.contagem}> ({total})</span>}
          </h2>

          {erro && <p className={styles.erro}>{erro}</p>}

          {carregando ? (
            <p className={styles.estado}>Carregando produtos...</p>
          ) : produtos.length === 0 ? (
            <p className={styles.estado}>Nenhum produto encontrado nessa categoria.</p>
          ) : (
            <div className={styles.grid}>
              {produtos.map((produto) => (
                <ProductCard key={produto.id} produto={produto} onAdicionar={adicionarAoCarrinho} />
              ))}
            </div>
          )}

          <Pagination paginaAtual={pagina} totalPaginas={totalPaginas} onMudarPagina={setPagina} />
        </section>

        <SobreContato />
      </main>

      <Footer />

      <CartDrawer
        aberto={carrinhoAberto}
        itens={itensCarrinho}
        onFechar={() => setCarrinhoAberto(false)}
        onAlterarQuantidade={alterarQuantidade}
        onRemover={removerDoCarrinho}
        onPedidoConfirmado={() => setItensCarrinho([])}
      />
    </div>
  );
}

export default function LojaPage() {
  return (
    <Suspense fallback={null}>
      <LojaConteudo />
    </Suspense>
  );
}
