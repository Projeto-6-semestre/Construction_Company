"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { RequireAuth } from "@/components/RequireAuth";
import { ApiError, atualizarProduto, criarProduto, getProdutos } from "@/lib/api";
import { iconeCategoria } from "@/lib/categorias";
import type { Produto, ProdutoCreateInput } from "@/types/api";
import styles from "./page.module.css";

const PRODUTO_VAZIO: ProdutoCreateInput = {
  sku: "",
  nome: "",
  categoria: "",
  unidade_medida: "un",
  quantidade_atual: 0,
  quantidade_minima: 0,
  preco_unitario: 0,
};

function Miniatura({ url, categoria }: { url: string; categoria: string }) {
  if (url) {
    // <img> simples em vez do componente Image do Next: aqui o valor muda a
    // cada tecla digitada (preview ao vivo), nao e uma imagem estatica
    // conhecida em build-time.
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={url}
        alt=""
        className={styles.miniaturaImg}
        onError={(e) => {
          e.currentTarget.style.display = "none";
        }}
      />
    );
  }
  return <span className={styles.miniaturaIcone}>{iconeCategoria(categoria)}</span>;
}

function LinhaProduto({ produto, onSalvo }: { produto: Produto; onSalvo: (p: Produto) => void }) {
  const [editando, setEditando] = useState(false);
  const [form, setForm] = useState({
    nome: produto.nome,
    categoria: produto.categoria,
    unidade_medida: produto.unidade_medida,
    quantidade_minima: produto.quantidade_minima,
    preco_unitario: produto.preco_unitario,
    preco_promocional: produto.preco_promocional ?? "",
    imagem_url: produto.imagem_url ?? "",
  });
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function salvar() {
    setSalvando(true);
    setErro(null);
    try {
      const atualizado = await atualizarProduto(produto.id, {
        nome: form.nome,
        categoria: form.categoria,
        unidade_medida: form.unidade_medida,
        quantidade_minima: Number(form.quantidade_minima),
        preco_unitario: Number(form.preco_unitario),
        preco_promocional: form.preco_promocional === "" ? null : Number(form.preco_promocional),
        imagem_url: form.imagem_url === "" ? null : form.imagem_url,
      });
      onSalvo(atualizado);
      setEditando(false);
    } catch (e) {
      setErro(e instanceof ApiError ? e.message : "Erro ao salvar.");
    } finally {
      setSalvando(false);
    }
  }

  if (!editando) {
    return (
      <tr>
        <td className={styles.celulaMiniatura}>
          <Miniatura url={produto.imagem_url ?? ""} categoria={produto.categoria} />
        </td>
        <td className={styles.sku}>{produto.sku}</td>
        <td>{produto.nome}</td>
        <td>{produto.categoria}</td>
        <td>{produto.quantidade_atual}</td>
        <td>{produto.quantidade_minima}</td>
        <td>R$ {produto.preco_unitario}</td>
        <td>{produto.preco_promocional ? `R$ ${produto.preco_promocional}` : "—"}</td>
        <td>
          <button className={styles.botaoEditar} onClick={() => setEditando(true)}>
            Editar
          </button>
        </td>
      </tr>
    );
  }

  return (
    <tr className={styles.linhaEditando}>
      <td className={styles.celulaMiniatura}>
        <Miniatura url={form.imagem_url} categoria={form.categoria} />
        <input
          className={styles.inputImagem}
          placeholder="URL da imagem"
          value={form.imagem_url}
          onChange={(e) => setForm({ ...form, imagem_url: e.target.value })}
        />
      </td>
      <td className={styles.sku}>{produto.sku}</td>
      <td>
        <input value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} />
      </td>
      <td>
        <input
          value={form.categoria}
          onChange={(e) => setForm({ ...form, categoria: e.target.value })}
        />
      </td>
      <td className={styles.somenteLeitura}>{produto.quantidade_atual}</td>
      <td>
        <input
          type="number"
          value={form.quantidade_minima}
          onChange={(e) => setForm({ ...form, quantidade_minima: e.target.value })}
        />
      </td>
      <td>
        <input
          type="number"
          step="0.01"
          value={form.preco_unitario}
          onChange={(e) => setForm({ ...form, preco_unitario: e.target.value })}
        />
      </td>
      <td>
        <input
          type="number"
          step="0.01"
          placeholder="sem promoção"
          value={form.preco_promocional}
          onChange={(e) => setForm({ ...form, preco_promocional: e.target.value })}
        />
      </td>
      <td className={styles.acoesEdicao}>
        {erro && <p className={styles.erroLinha}>{erro}</p>}
        <div className={styles.botoesLinha}>
          <button className={styles.botaoSalvar} onClick={salvar} disabled={salvando}>
            {salvando ? "Salvando..." : "Salvar"}
          </button>
          <button className={styles.botaoCancelar} onClick={() => setEditando(false)}>
            Cancelar
          </button>
        </div>
      </td>
    </tr>
  );
}

function PainelProdutos() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [novo, setNovo] = useState<ProdutoCreateInput>(PRODUTO_VAZIO);
  const [criando, setCriando] = useState(false);
  const [erroCriar, setErroCriar] = useState<string | null>(null);

  function carregar() {
    setCarregando(true);
    getProdutos()
      .then(setProdutos)
      .catch((e) => setErro(e instanceof ApiError ? e.message : "Erro ao carregar produtos."))
      .finally(() => setCarregando(false));
  }

  useEffect(carregar, []);

  async function criar(e: React.FormEvent) {
    e.preventDefault();
    setCriando(true);
    setErroCriar(null);
    try {
      await criarProduto(novo);
      setNovo(PRODUTO_VAZIO);
      carregar();
    } catch (e) {
      setErroCriar(e instanceof ApiError ? e.message : "Erro ao criar produto.");
    } finally {
      setCriando(false);
    }
  }

  function atualizarNaLista(produto: Produto) {
    setProdutos((atual) => atual.map((p) => (p.id === produto.id ? produto : p)));
  }

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <div>
          <h1>Gerenciar produtos</h1>
          <p>Cadastre novos produtos, ajuste preço, promoção e imagem do catálogo.</p>
        </div>
        <Link href="/" className={styles.link}>
          ← Voltar ao painel
        </Link>
      </header>

      <form className={styles.formNovo} onSubmit={criar}>
        <h2>Novo produto</h2>
        <div className={styles.gridForm}>
          <input
            placeholder="SKU"
            value={novo.sku}
            onChange={(e) => setNovo({ ...novo, sku: e.target.value })}
            required
          />
          <input
            placeholder="Nome"
            value={novo.nome}
            onChange={(e) => setNovo({ ...novo, nome: e.target.value })}
            required
          />
          <input
            placeholder="Categoria"
            value={novo.categoria}
            onChange={(e) => setNovo({ ...novo, categoria: e.target.value })}
            required
          />
          <input
            placeholder="Unidade (un, saco, m3...)"
            value={novo.unidade_medida}
            onChange={(e) => setNovo({ ...novo, unidade_medida: e.target.value })}
            required
          />
          <input
            type="number"
            placeholder="Quantidade inicial"
            value={novo.quantidade_atual}
            onChange={(e) => setNovo({ ...novo, quantidade_atual: Number(e.target.value) })}
          />
          <input
            type="number"
            placeholder="Estoque mínimo"
            value={novo.quantidade_minima}
            onChange={(e) => setNovo({ ...novo, quantidade_minima: Number(e.target.value) })}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Preço unitário"
            value={novo.preco_unitario || ""}
            onChange={(e) => setNovo({ ...novo, preco_unitario: Number(e.target.value) })}
            required
          />
          <input
            placeholder="URL da imagem (opcional)"
            value={novo.imagem_url ?? ""}
            onChange={(e) => setNovo({ ...novo, imagem_url: e.target.value })}
          />
        </div>
        {erroCriar && <p className={styles.erro}>{erroCriar}</p>}
        <button type="submit" className={styles.botaoCriar} disabled={criando}>
          {criando ? "Criando..." : "Cadastrar produto"}
        </button>
      </form>

      <section>
        <h2>Catálogo ({produtos.length})</h2>
        {erro && <p className={styles.erro}>{erro}</p>}
        {carregando ? (
          <p className={styles.estado}>Carregando...</p>
        ) : (
          <div className={styles.tabelaScroll}>
            <table className={styles.tabela}>
              <thead>
                <tr>
                  <th>Imagem</th>
                  <th>SKU</th>
                  <th>Nome</th>
                  <th>Categoria</th>
                  <th>Estoque</th>
                  <th>Mínimo</th>
                  <th>Preço</th>
                  <th>Promoção</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {produtos.map((produto) => (
                  <LinhaProduto key={produto.id} produto={produto} onSalvo={atualizarNaLista} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}

export default function ProdutosPage() {
  return (
    <RequireAuth>
      <PainelProdutos />
    </RequireAuth>
  );
}
