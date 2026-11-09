<div align="center">

<img src="frontend/public/images/logo.png" alt="Logo Agente de Estoque" width="110" />

# 🧱 AGENTE DE ESTOQUE
### Sistema de Controle de Estoque com Agente de IA para Materiais de Construção

[![Acessar Loja](https://img.shields.io/badge/🛒_Acessar_Loja-Vercel-000000?style=for-the-badge&logo=vercel)](https://construction-company-liard.vercel.app/loja)
[![API Online](https://img.shields.io/badge/⚙️_API_Online-Render-46E3B7?style=for-the-badge&logo=render)](https://construction-company-ljfz.onrender.com/docs)
[![Vídeo Demo](https://img.shields.io/badge/▶️_Vídeo_Demo-em_breve-red?style=for-the-badge&logo=youtube)](./ROTEIRO_VIDEO.md)

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=for-the-badge&logo=postgresql)](https://neon.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Groq-1C3C3C?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Curso:** Ciência da Computação | **Período:** [preencher] | **Semestre:** 6º | **Ano:** 2026 | **Instituição:** UNINOVE — Projeto de Extensão

</div>

---

## 👥 Equipe e Papéis

<div align="center">

| Integrante | RA | Papel Principal | Principais Entregas |
|:----------:|:--:|:----------------:|:--------------------:|
| **Eduardo Daniel** | `[preencher]` | 🔧 Backend / DevOps | API (`app/`), CI/CD, deploy (Vercel/Render/Neon) |
| **Eduardo Matheus** | `[preencher]` | 🎨 Front-end | Loja pública e painel interno (`frontend/`) |
| **João** | `[preencher]` | 🗄️ Banco de Dados | Modelagem (`app/models/`), migrations (`migrations/`) |
| **Carlos** | `[preencher]` | ✅ QA / Qualidade | Testes de integração, checklist de testes manuais |
| **Diogo** | `[preencher]` | 📄 Documentação ABNT + Vídeo | Relatório final, roteiro e gravação do vídeo |
| **Josué** | `[preencher]` | 📝 Apoio à Documentação | README, guia do projeto, plano de trabalho |

</div>

---

<a name="motivacao"></a>
## 💭 Por Que Este Projeto Existe?

### 🧱 O Problema de Quem Vende Material de Construção

Lojas pequenas e médias de materiais de construção, na maioria das vezes, controlam estoque de um jeito manual: caderno, planilha solta, ou simplesmente "de cabeça". O resultado é previsível — vendedor promete um produto que não tem mais, cliente liga pra saber se tem cimento disponível e ninguém sabe responder na hora, e pedidos anotados em papel se perdem.

### 📉 A Realidade que Nos Motivou

Durante o planejamento do projeto, olhamos pra um protótipo de referência mais simples (um agente de IA sobre um CSV estático, sem banco de dados, sem testes, sem separação de camadas) e enxergamos exatamente os problemas que uma loja de verdade teria se dependesse de algo parecido: nenhuma garantia de que o número de estoque é real, nenhum histórico de quem comprou o quê, e nenhuma forma seria de o cliente comprar sem ligar.

<div align="center">

```mermaid
graph LR
    A[😟 Cliente quer comprar] --> B[📞 Liga pra loja]
    B --> C[❓ Vendedor não tem certeza do estoque]
    C --> D[😤 Cliente desiste ou compra errado]

    A2[😊 Cliente quer comprar] --> F[🛒 Loja online]
    F --> G[📦 Estoque real, sempre atualizado]
    G --> H[✅ Pedido confirmado na hora]

    style A fill:#ffcccc
    style D fill:#ffcccc
    style A2 fill:#ccffcc
    style H fill:#ccffcc
```

</div>

### 💡 A Solução: Estoque que Nunca Mente

E se **toda** entrada e saída de material — venda, reposição de fornecedor, pedido feito pelo chat — passasse obrigatoriamente pelo mesmo sistema, em vez de depender de alguém atualizar uma planilha depois?

Foi assim que nasceu o **Agente de Estoque**: uma API que centraliza todo o controle, com um **agente de IA** que conversa em linguagem natural pra consultar estoque e registrar pedidos, uma **loja pública** onde o cliente compra direto, e um **painel interno** onde a equipe acompanha tudo — estoque, pedidos e um dashboard de entradas/saídas.

### 🎯 O Impacto Real

<table>
<tr>
<td width="33%" align="center">

#### 🧑‍🤝‍🧑 Para o Cliente
✅ Compra sem precisar ligar
✅ Vê o estoque real na loja
✅ Pedido confirmado na hora
✅ Resumo do pedido direto no WhatsApp

</td>
<td width="33%" align="center">

#### 🏪 Para a Loja
✅ Estoque sempre correto
✅ Zero planilha solta
✅ Histórico de toda movimentação
✅ Dashboard pra "fazer as contas"

</td>
<td width="33%" align="center">

#### 👷 Para a Equipe
✅ Chat de IA tira dúvida rápida
✅ Painel central de pedidos
✅ Sem retrabalho de contagem manual
✅ Login próprio e seguro

</td>
</tr>
</table>

### 🚀 Nossa Missão

<div align="center">

> ### *"Um número de estoque em que dá pra confiar"*
>
> Queremos que nenhuma venda se perca por falta de informação,
> que o estoque mostrado seja sempre o estoque real,
> e que uma loja pequena consiga vender online sem precisar de um sistema caro.

</div>

---

## 📖 Índice

- [💭 Por Que Este Projeto Existe?](#motivacao)
- [🎯 Sobre o Projeto](#sobre)
- [❓ Problema](#problema)
- [🤖 Tecnologias](#tecnologias)
- [🗄️ Modelo de Dados](#dados)
- [🏗️ Arquitetura](#arquitetura)
- [⚙️ Como Rodar Localmente](#instalacao)
- [🌐 Acessar Online](#online)
- [📸 Telas do Sistema](#screenshots)
- [📈 Status e Resultados](#resultados)
- [🎥 Vídeo de Demonstração](#video)
- [💡 Decisões Técnicas](#decisoes)
- [📚 Referências](#referencias)
- [📄 Licença](#licenca)
- [🙏 Agradecimentos](#agradecimentos)

---

<a name="sobre"></a>
## 🎯 Sobre o Projeto

> Sistema web completo pra controle de estoque de uma empresa de materiais de construção: **loja pública** (catálogo + carrinho + checkout via WhatsApp), **painel interno** (gestão de produtos, pedidos e dashboard) e um **agente de IA** que consulta estoque e registra pedidos por chat — sem nunca gerar SQL ou código livre, só escolhendo entre um conjunto fixo de ferramentas seguras.

### ✨ Destaques

```mermaid
graph LR
    A[🧑 Cliente] --> B[🛒 Loja Pública]
    B --> C[📦 Pedido]
    C --> D[📲 WhatsApp]
    C --> E[🗄️ Banco de Dados]

    F[👷 Funcionário] --> G[💬 Chat com Agente de IA]
    F --> H[📊 Dashboard]
    G --> E
    H --> E

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e1ffe1
    style F fill:#ffe1e1
    style G fill:#f0e1ff
    style H fill:#ffe1f0
```

---

<a name="problema"></a>
## ❓ Problema

### 📋 Contexto

Controle de estoque manual em pequenas lojas de material de construção gera erro, venda perdida e retrabalho. Hoje:

| ❌ Situação sem o sistema | ✅ Com o Agente de Estoque |
|---|---|
| Contagem manual, sujeita a erro humano | Toda entrada/saída passa pelo sistema — número sempre real |
| Cliente liga pra saber se tem material disponível | Loja pública mostra o catálogo e o estoque em tempo real |
| Pedido anotado em papel ou WhatsApp solto, fácil de perder | Pedido gravado no banco + resumo no WhatsApp, visível no painel |
| Sem noção de quanto entrou/saiu em valor | Dashboard com entradas, saídas e saldo estimado por categoria |
| Atendimento por IA sem controle (risco de gerar SQL/código perigoso) | Agente de IA só escolhe entre ferramentas fixas e seguras |

### 🎯 Objetivo

Construir um sistema que:
1. Garante que o **estoque mostrado é sempre o estoque real** (toda mudança passa pelo mesmo serviço, nunca é editada direto no banco).
2. Permite que o **cliente compre sozinho**, sem depender de atendimento por telefone.
3. Dá à equipe um **agente de IA seguro** — tool-calling fixo, nunca execução livre de código.
4. Oferece **visibilidade financeira básica** (dashboard) sem precisar de um ERP caro.

---

<a name="tecnologias"></a>
## 🤖 Tecnologias

### 🏗️ Arquitetura em Camadas

```mermaid
flowchart TB
    subgraph Frontend["🔵 FRONT-END — Next.js / React"]
        F1[Loja pública] 
        F2[Painel interno]
        F3[Chat com o Agente]
    end

    subgraph Backend["🟢 BACK-END — FastAPI / Python"]
        B1["api/ — rotas HTTP"] --> B2["services/ — regra de negócio"]
        B2 --> B3["repositories/ — acesso a dados"]
        B3 --> B4["models/ — tabelas SQLAlchemy"]
        B2 --> B5["agent/ — LangChain + Groq"]
    end

    subgraph Dados["🟡 DADOS"]
        D1[("PostgreSQL + pgvector<br/>(Neon)")]
    end

    Frontend -- HTTP / JSON --> Backend
    Backend --> Dados

    style Frontend fill:#e3f2fd
    style Backend fill:#e8f5e9
    style Dados fill:#fff3e0
```

### 📚 Stack Tecnológico

<div align="center">

| Categoria | Tecnologia | Função |
|:---:|:---:|:---:|
| **Back-end** | FastAPI (Python 3.12, assíncrono) | API REST |
| **ORM / Migrations** | SQLAlchemy 2.x (async) + Alembic | Mapeamento e versionamento do banco |
| **Banco de dados** | PostgreSQL + pgvector (hospedado no Neon) | Armazenamento relacional |
| **Agente de IA** | LangChain + Groq (API compatível OpenAI) | Chat com tool-calling seguro |
| **Front-end** | React + Next.js (App Router) | Interface web |
| **Gráficos** | Recharts | Dashboard de entradas/saídas |
| **Empacotamento** | `pyproject.toml` + `uv` | Dependências e lockfile |
| **Testes** | pytest + pytest-asyncio | Testes automatizados (back-end) |
| **Lint** | ruff (back-end) + ESLint (front-end) | Qualidade de código |
| **CI/CD** | GitHub Actions | Lint + testes a cada push/PR |
| **Deploy** | Vercel + Render + Neon | Hospedagem gratuita, front/back/banco separados |

</div>

### 🧠 Por que o agente de IA nunca gera código livre?

O protótipo de referência que inspirou esse projeto executava código Python gerado pelo próprio modelo de linguagem, sem sandbox — uma escolha arriscada fora de um ambiente 100% local. Aqui, o agente **só escolhe qual ferramenta chamar** entre um conjunto fixo (`consultar_estoque`, `registrar_pedido`, `repor_estoque`) e com quais argumentos. Quem grava no banco é sempre código Python determinístico nosso — nunca o modelo diretamente.

---

<a name="dados"></a>
## 🗄️ Modelo de Dados

<div align="center">

| Tabela | O que guarda |
|:---:|:---|
| `produtos` | Catálogo: SKU, nome, categoria, estoque atual/mínimo, preço (e promoção/imagem) |
| `fornecedores` | Quem entrega material — criado automaticamente na reposição de estoque |
| `pedidos` | Pedidos feitos por clientes (loja pública ou chat) |
| `itens_pedido` | Itens de cada pedido (produto + quantidade) |
| `movimentacoes_estoque` | Histórico de **toda** entrada e saída — é a auditoria que garante o número real |
| `usuarios` | Login do painel interno (funcionários) — não existe cadastro público de propósito |

</div>

`quantidade` e `preço` usam `NUMERIC` (não `float`) em todo o banco — erro de arredondamento em estoque ou dinheiro não é aceitável.

---

<a name="arquitetura"></a>
## 🏗️ Arquitetura do Sistema

### 📁 Estrutura de Pastas

```
Construction_Company/
├── 📄 README.md                 ← Você está aqui!
├── 📄 GUIA_PROJETO.md           ← Guia completo de workflow do time
├── 📄 COMO_COMECAR.md           ← Onboarding pra quem entra no time
├── 📄 DEPLOY.md                 ← Passo a passo do deploy (Vercel/Render/Neon)
├── 📄 ROTEIRO_VIDEO.md          ← Roteiro do vídeo de apresentação
├── 📄 render.yaml               ← Config do back-end no Render
├── 📄 Dockerfile / docker-compose.yml
│
├── 🐍 app/                      ← BACK-END (Python / FastAPI)
│   ├── api/routes/              ← Rotas HTTP (auth, produtos, pedidos, dashboard, chat)
│   ├── services/                ← Regra de negócio (único lugar que muda estoque)
│   ├── repositories/            ← Acesso ao banco, sem decidir nada
│   ├── models/                  ← Tabelas (SQLAlchemy) + schemas (Pydantic)
│   ├── agent/                   ← Agente de IA (LangChain + Groq, tool-calling)
│   ├── rag/                     ← Reservado p/ busca documental futura (pgvector)
│   └── core/                    ← Configuração, conexão com banco, segurança
│
├── 🔄 migrations/               ← Histórico versionado do banco (Alembic)
│
├── ⚛️ frontend/                  ← FRONT-END (TypeScript / Next.js)
│   ├── app/                     ← Páginas: loja, produtos, pedidos, dashboard, login
│   ├── components/              ← Componentes (loja pública + painel interno)
│   └── lib/                     ← Funções que chamam a API do back-end
│
├── 🧪 tests/unit/                ← Testes automatizados (SQLite em memória, sem rede)
├── 🧰 scripts/                   ← Seed de dados, criação de usuário admin
└── 📚 docsprojeto/               ← Material da professora (ABNT, orientações)
```

### 🔄 Fluxo de uma Pergunta no Chat

```mermaid
sequenceDiagram
    participant U as 👷 Funcionário
    participant C as 💬 Chat
    participant A as 🤖 Agente (LangChain)
    participant S as ⚙️ Service
    participant R as 🗄️ Repository
    participant DB as 🐘 PostgreSQL

    U->>C: "Qual o estoque de cimento?"
    C->>A: pergunta + histórico
    A->>A: decide chamar a ferramenta consultar_estoque
    A->>S: consultar_estoque(categoria="cimento")
    S->>R: list_produtos(...)
    R->>DB: SELECT ...
    DB->>R: linhas
    R->>S: lista de produtos
    S->>A: resultado
    A->>C: resposta em linguagem natural
    C->>U: "Temos 300 sacos de CIMENTO-50KG em estoque"
```

### 🛒 Fluxo de Compra na Loja

```mermaid
sequenceDiagram
    participant Cl as 🧑 Cliente
    participant L as 🛒 Loja (Next.js)
    participant API as ⚙️ API (FastAPI)
    participant DB as 🐘 PostgreSQL
    participant W as 📲 WhatsApp

    Cl->>L: Monta carrinho + nome
    L->>API: POST /pedidos
    API->>DB: Valida estoque de TODOS os itens
    alt estoque suficiente
        API->>DB: Grava pedido + baixa estoque
        API->>L: Pedido confirmado
        L->>W: Abre resumo do pedido pronto pra enviar
    else estoque insuficiente
        API->>L: Erro 409 com os itens faltantes
    end
```

---

<a name="instalacao"></a>
## ⚙️ Como Rodar Localmente

### 📋 Pré-requisitos

- Python 3.12+
- Node.js 20+
- Docker Desktop (banco de dados local)
- `uv` (gerenciador de pacotes Python) — `pip install uv`

### 🚀 Passo a Passo

#### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Projeto-6-semestre/Construction_Company.git
cd Construction_Company
```

#### 2️⃣ Configurar o back-end
```bash
uv sync
cp .env.example .env
# edite o .env e preencha GROQ_API_KEY (gratuito em console.groq.com/keys)
```

#### 3️⃣ Subir o banco e rodar as migrations
```bash
docker compose up -d db
uv run alembic upgrade head
uv run python scripts/seed_data.py   # opcional: dados de demonstração
```

#### 4️⃣ Rodar a API
```bash
uv run uvicorn app.main:app --reload
```
Disponível em `http://localhost:8000` — docs interativas em `http://localhost:8000/docs`.

#### 5️⃣ Rodar o front-end
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
Disponível em `http://localhost:3000`.

#### 🧪 Rodar os testes
```bash
uv run pytest tests/unit
```

#### 🐳 Tudo via Docker Compose
```bash
docker compose up --build
```

Guia completo de onboarding em [`COMO_COMECAR.md`](./COMO_COMECAR.md).

---

<a name="online"></a>
## 🌐 Acessar Online

O projeto está no ar de verdade, sem precisar instalar nada — front-end, back-end e banco de dados cada um no seu próprio serviço gratuito:

<div align="center">

| Parte | Onde roda | Link |
|:---:|:---:|:---:|
| 🛒 **Loja pública** (cliente) | Vercel | [construction-company-liard.vercel.app/loja](https://construction-company-liard.vercel.app/loja) |
| 👷 **Painel interno** (funcionário, exige login) | Vercel | [construction-company-liard.vercel.app/login](https://construction-company-liard.vercel.app/login) |
| ⚙️ **API** (documentação Swagger) | Render | [construction-company-ljfz.onrender.com/docs](https://construction-company-ljfz.onrender.com/docs) |
| 🗄️ **Banco de dados** | Neon | PostgreSQL gerenciado (acesso interno) |

</div>

> ⚠️ O back-end roda no plano gratuito do Render, que "dorme" depois de ~15 minutos sem uso — a primeira requisição depois disso pode demorar até 1 minuto pra responder. É normal, espera carregar.

Passo a passo completo de como esse deploy foi montado em [`DEPLOY.md`](./DEPLOY.md).

---

<a name="screenshots"></a>
## 📸 Telas do Sistema

> 🚧 Prints a adicionar aqui depois da gravação do vídeo de demonstração (ver [`ROTEIRO_VIDEO.md`](./ROTEIRO_VIDEO.md)).

- Loja pública (catálogo + carrinho)
- Painel interno (estoque + chat com o agente de IA)
- Tela de pedidos
- Dashboard de entradas/saídas

---

<a name="resultados"></a>
## 📈 Status e Resultados

<div align="center">

| Item | Status |
|:---|:---:|
| Autenticação (JWT) | ✅ |
| CRUD de produtos | ✅ |
| Loja pública com carrinho | ✅ |
| Checkout com redirecionamento pro WhatsApp | ✅ |
| Agente de IA (consulta + registro de pedido via chat) | ✅ |
| Painel de pedidos | ✅ |
| Dashboard de entradas/saídas | ✅ |
| Testes automatizados | ✅ 18/18 passando |
| CI (lint + testes a cada push/PR) | ✅ |
| Deploy ao vivo (Vercel + Render + Neon) | ✅ |
| Testes de integração (Postgres real) | ⏳ pendente |
| Relatório final (ABNT) | ⏳ pendente |

</div>

### ⏱️ Performance

| Métrica | Valor |
|---|---|
| Testes unitários (back-end) | 18/18 passando, ~1.8s |
| Build do front-end | ~1s (Turbopack) |
| Cold start da API (Render, após dormir) | ~50s (plano gratuito) |

---

<a name="video"></a>
## 🎥 Vídeo de Demonstração

<div align="center">

### 🎬 Em breve

[![Vídeo no YouTube](https://img.shields.io/badge/YouTube-link_em_breve-red?style=for-the-badge&logo=youtube)](./ROTEIRO_VIDEO.md)

**Roteiro completo:** [`ROTEIRO_VIDEO.md`](./ROTEIRO_VIDEO.md)

**Conteúdo previsto:**
1. 👋 Apresentação da equipe e motivação do projeto
2. 🛒 Demonstração da loja pública (carrinho → WhatsApp)
3. 💬 Demonstração do painel interno e do chat com o agente de IA
4. 📊 Demonstração do dashboard de entradas/saídas
5. 🏗️ Arquitetura e organização do código
6. 🌐 Prova de que o sistema está no ar (Vercel + Render)

</div>

---

<a name="decisoes"></a>
## 💡 Decisões Técnicas

| Decisão | Por quê |
|---|---|
| **Groq** em vez de Hugging Face pro LLM | A Hugging Face removeu o crédito gratuito mensal; a Groq mantém tier gratuito de verdade e bom suporte a tool-calling |
| `NUMERIC`/`Decimal`, nunca `float`, pra estoque e preço | Erro de arredondamento em estoque significa contar material que não existe |
| Agente de IA só com tool-calling fixo | Executar código/SQL livre gerado por LLM é risco de segurança — o protótipo de referência fazia isso sem sandbox |
| `SELECT ... FOR UPDATE` ao baixar estoque | Evita condição de corrida em dois pedidos simultâneos pro mesmo produto |
| Valor do dashboard = quantidade × **preço atual** | O histórico de movimentação não guarda o preço de quando aconteceu — é deixado explícito na tela que é uma estimativa, não contabilidade exata |
| Migration roda automaticamente no deploy (`Dockerfile`) | Único ambiente de demonstração (não produção real com usuários pagantes); mais simples que migration manual nesse contexto |
| Deploy em 3 serviços gratuitos separados (Vercel + Render + Neon) | A Vercel não hospeda bem um back-end com conexão persistente ao banco; cada serviço faz a parte que faz melhor, de graça |
| Repositório público no GitHub | Necessário pro plano gratuito da Vercel aceitar deploy de repositório de organização |

---

<a name="referencias"></a>
## 📚 Referências

### 📖 Documentação oficial das tecnologias usadas

- [FastAPI](https://fastapi.tiangolo.com/) — framework do back-end
- [SQLAlchemy](https://docs.sqlalchemy.org/) — ORM assíncrono
- [Alembic](https://alembic.sqlalchemy.org/) — migrations de banco
- [LangChain](https://python.langchain.com/) — orquestração do agente de IA
- [Groq](https://console.groq.com/docs) — provedor do modelo de linguagem
- [Next.js](https://nextjs.org/docs) — framework do front-end
- [Recharts](https://recharts.org/) — gráficos do dashboard
- [Render](https://render.com/docs) / [Vercel](https://vercel.com/docs) / [Neon](https://neon.com/docs) — hospedagem do deploy gratuito

### 🎓 Acadêmicas

**Orientação:**
- **Prof(a). [preencher]**
  Projeto de Extensão — 6º Semestre — Ciência da Computação
  Instituição: UNINOVE

---

<a name="licenca"></a>
## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License - Copyright (c) 2026 Projeto Agente de Estoque — Materiais de Construção
```

---

<a name="agradecimentos"></a>
## 🙏 Agradecimentos

<div align="center">

### Nossos sinceros agradecimentos a todos que contribuíram para este projeto:

</div>

- 🎓 **Prof(a). [preencher]**
  Orientação técnica e acadêmica do projeto de extensão

- 🏫 **UNINOVE**
  Suporte acadêmico e infraestrutura para o desenvolvimento

- 🤖 **Comunidade Open Source**
  Pelas ferramentas que tornaram esse projeto possível: FastAPI, SQLAlchemy, Alembic, LangChain, Next.js, React e Recharts

---

**Este projeto não seria possível sem o esforço de toda a equipe e o apoio da comunidade open source!**

---

## 📞 Contato

<div align="center">

**Dúvidas ou sugestões?**

[![GitHub](https://img.shields.io/badge/GitHub-Construction__Company-black?style=for-the-badge&logo=github)](https://github.com/Projeto-6-semestre/Construction_Company)
[![Email](https://img.shields.io/badge/Email-Contato-red?style=for-the-badge&logo=gmail)](mailto:edwardpf02@gmail.com)

</div>

---

<div align="center">

### ⭐ Se este projeto te ajudou, deixe uma estrela!

![GitHub Stars](https://img.shields.io/github/stars/Projeto-6-semestre/Construction_Company?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Projeto-6-semestre/Construction_Company?style=social)
![GitHub Watchers](https://img.shields.io/github/watchers/Projeto-6-semestre/Construction_Company?style=social)

</div>
