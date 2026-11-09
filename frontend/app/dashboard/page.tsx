"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { RequireAuth } from "@/components/RequireAuth";
import { ApiError, getDashboard } from "@/lib/api";
import type { DashboardResponse } from "@/types/api";
import styles from "./page.module.css";

// Par categorico validado (CVD-safe, contraste >=3:1 no fundo escuro do painel)
// via scripts/validate_palette.js da skill de dataviz - nao trocar sem revalidar.
const COR_ENTRADAS = "#3987e5";
const COR_SAIDAS = "#d95926";

function formatarMoeda(valor: string | number): string {
  return Number(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function formatarData(iso: string): string {
  return new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Tela do painel interno: visao geral de quanto entrou e quanto saiu do
// estoque, pra equipe ter base pra fazer contas - nao e contabilidade exata
// (valor usa o preco ATUAL do produto, nao o preco de quando a movimentacao
// aconteceu, que o banco nao guarda), e isso fica avisado na tela.
function PainelDashboard() {
  const [dados, setDados] = useState<DashboardResponse | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    getDashboard()
      .then(setDados)
      .catch((e) => setErro(e instanceof ApiError ? e.message : "Erro ao carregar o dashboard."))
      .finally(() => setCarregando(false));
  }, []);

  const saldo = dados ? Number(dados.valor_entradas) - Number(dados.valor_saidas) : 0;

  const dadosGrafico =
    dados?.por_categoria.map((c) => ({
      categoria: c.categoria,
      Entradas: Number(c.valor_entradas),
      Saídas: Number(c.valor_saidas),
    })) ?? [];

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <div>
          <h1>Dashboard</h1>
          <p>
            Visão geral de entradas e saídas de estoque — valor estimado pelo{" "}
            <strong>preço atual</strong> de cada produto (não é o preço de quando a movimentação
            aconteceu).
          </p>
        </div>
        <Link href="/" className={styles.link}>
          ← Voltar ao painel
        </Link>
      </header>

      {erro && <p className={styles.erro}>{erro}</p>}

      {carregando || !dados ? (
        <p className={styles.estado}>Carregando...</p>
      ) : (
        <>
          <div className={styles.tiles}>
            <div className={styles.tile}>
              <span className={styles.tileLabel}>Entradas (valor estimado)</span>
              <span className={styles.tileValor} style={{ color: COR_ENTRADAS }}>
                {formatarMoeda(dados.valor_entradas)}
              </span>
              <span className={styles.tileSub}>{dados.total_entradas_qtd} unidades</span>
            </div>
            <div className={styles.tile}>
              <span className={styles.tileLabel}>Saídas (valor estimado)</span>
              <span className={styles.tileValor} style={{ color: COR_SAIDAS }}>
                {formatarMoeda(dados.valor_saidas)}
              </span>
              <span className={styles.tileSub}>{dados.total_saidas_qtd} unidades</span>
            </div>
            <div className={styles.tile}>
              <span className={styles.tileLabel}>Saldo (entradas − saídas)</span>
              <span
                className={styles.tileValor}
                style={{ color: saldo >= 0 ? COR_ENTRADAS : COR_SAIDAS }}
              >
                {formatarMoeda(saldo)}
              </span>
              <span className={styles.tileSub}>desde o início</span>
            </div>
          </div>

          {dadosGrafico.length > 0 && (
            <section className={styles.graficoCard}>
              <h2>Entradas × Saídas por categoria</h2>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={dadosGrafico} barCategoryGap="22%" barGap={2}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
                  <XAxis dataKey="categoria" stroke="#8b93a1" fontSize={12} tickLine={false} />
                  <YAxis
                    stroke="#8b93a1"
                    fontSize={12}
                    tickLine={false}
                    width={80}
                    tickFormatter={(v) => formatarMoeda(v)}
                  />
                  <Tooltip
                    cursor={{ fill: "rgba(255,255,255,0.04)" }}
                    contentStyle={{
                      background: "#1b212a",
                      border: "1px solid rgba(255,255,255,0.15)",
                      borderRadius: 8,
                      color: "#f2f0ea",
                      fontSize: 13,
                    }}
                    formatter={(valor) => formatarMoeda(Number(valor))}
                  />
                  <Legend wrapperStyle={{ fontSize: 13, color: "#c4cad3" }} />
                  <Bar dataKey="Entradas" fill={COR_ENTRADAS} radius={[4, 4, 0, 0]} maxBarSize={48} />
                  <Bar dataKey="Saídas" fill={COR_SAIDAS} radius={[4, 4, 0, 0]} maxBarSize={48} />
                </BarChart>
              </ResponsiveContainer>
            </section>
          )}

          <section>
            <h2 className={styles.secaoTitulo}>Movimentações recentes</h2>
            {dados.recentes.length === 0 ? (
              <p className={styles.estado}>Nenhuma movimentação ainda.</p>
            ) : (
              <div className={styles.tabelaScroll}>
                <table className={styles.tabela}>
                  <thead>
                    <tr>
                      <th>Data</th>
                      <th>Tipo</th>
                      <th>Produto</th>
                      <th>Quantidade</th>
                      <th>Motivo / Fornecedor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dados.recentes.map((mov) => (
                      <tr key={mov.id}>
                        <td>{formatarData(mov.criado_em)}</td>
                        <td>
                          <span className={mov.tipo === "entrada" ? styles.tagEntrada : styles.tagSaida}>
                            {mov.tipo === "entrada" ? "Entrada" : "Saída"}
                          </span>
                        </td>
                        <td>
                          {mov.produto.nome} <span className={styles.sku}>({mov.produto.sku})</span>
                        </td>
                        <td>{mov.quantidade}</td>
                        <td>{mov.fornecedor ? mov.fornecedor.nome : (mov.motivo ?? "—")}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </main>
  );
}

export default function DashboardPage() {
  return (
    <RequireAuth>
      <PainelDashboard />
    </RequireAuth>
  );
}
