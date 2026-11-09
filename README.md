# Agente de Estoque — Materiais de Construção

> Agente de IA via chat para controle de estoque de uma empresa de materiais de construção (blocos, cimento, areia, ferramentas). O agente sempre sabe o número certo de estoque porque toda entrada/saída passa por ele — sem contagem manual.

## Estrutura do projeto

O projeto é dividido em 3 partes **separadas**, que conversam só por HTTP (nunca código misturado no mesmo arquivo):

| Pasta | O que é | Linguagem |
|---|---|---|
| [`app/`](./app) | **Back-end** — API, regra de negócio, agente de IA | Python (FastAPI) |
| [`frontend/`](./frontend) | **Front-end** — telas, loja, painel interno | TypeScript (React/Next.js) |
| [`migrations/`](./migrations) + Docker (`db`) | **Banco de dados** — estrutura das tabelas e dados | PostgreSQL + Alembic |

Dentro do back-end (`app/`), as camadas também são separadas:

```
app/
├── api/            rotas HTTP (o que o front-end chama)
├── services/       regra de negócio (ex: "só confirma pedido se tiver estoque")
├── agent/          agente de IA (chat) — só escolhe ferramentas, nunca gera SQL/código livre
├── repositories/   acesso ao banco de dados
├── models/         tabelas do banco (SQLAlchemy) + validação de dados (Pydantic)
└── core/           configuração, conexão com banco, logging
```

Pastas como `__pycache__/`, `.venv/`, `node_modules/` e `.next/` **não são código** — são arquivos gerados automaticamente ao rodar o projeto (cache do Python, dependências instaladas). Elas não entram no Git (ver `.gitignore`) e ficam ocultas no explorer do VSCode (ver `.vscode/settings.json`).

## Status atual do projeto

- [x] Estrutura de pastas e guia de workflow do projeto
- [x] Repositório criado na organização GitHub
- [x] Stack definida: FastAPI + SQLAlchemy/Alembic + PostgreSQL (pgvector reservado) + Groq + React/Next.js
- [x] Banco de dados + migrations (produtos, fornecedores, pedidos, itens_pedido, movimentacoes_estoque, usuarios)
- [x] Camada de serviço com regra de negócio (pedido só confirma se TODOS os itens tiverem estoque)
- [x] Agente de IA via LangChain (tool-calling, sem execução de código/SQL livre)
- [x] Autenticação do painel interno (login + JWT)
- [x] CRUD de produtos (cadastro, edição, promoção/imagem) no painel interno
- [x] Loja pública com catálogo paginado, categorias, carrinho e fechamento de pedido
- [x] API FastAPI (`/health`, `/auth`, `/produtos`, `/pedidos`, `/chat`)
- [x] Frontend React/Next.js (loja pública, painel interno, login, chat)
- [x] Código comentado em português (back-end e front-end)
- [x] CI rodando lint (ruff/eslint) e testes automaticamente a cada push/PR
- [x] Testes unitários da camada de serviço e autenticação
- [ ] Testes de integração contra Postgres real (`tests/integration/` ainda vazio)
- [ ] Deploy em homologação e produção (VPS, Nginx, HTTPS, workflows de deploy)
- [ ] Relatório final do projeto (modelo ABNT em `docsprojeto/`)

Roadmap completo em [`GUIA_PROJETO.md`](./GUIA_PROJETO.md), seção 10. Detalhes de papéis/responsabilidades em [`docs/plano-de-trabalho.pdf`](./docs/plano-de-trabalho.pdf) — **ainda com os campos "Responsável" em branco, falta o time preencher com os nomes de cada um**.

## Stack

Python 3.12+ · FastAPI (async) · SQLAlchemy 2.x + Alembic · PostgreSQL (`pgvector/pgvector:pg16`) · LangChain + Groq (`llama-3.3-70b-versatile`) · React + Next.js · `uv` · pytest · Docker.

## Como rodar localmente

### Backend

```powershell
# 1. Instalar dependencias
uv sync

# 2. Copiar e preencher o .env (precisa de uma chave gratuita da Groq - console.groq.com/keys)
cp .env.example .env
# edite .env e preencha GROQ_API_KEY

# 3. Subir o banco
docker compose up -d db

# 4. Rodar as migrations
uv run alembic upgrade head

# 5. (opcional) popular com dados de demonstracao
uv run python scripts/seed_data.py

# 6. Rodar a API
uv run uvicorn app.main:app --reload
```

API disponível em `http://localhost:8000`, docs interativas em `http://localhost:8000/docs`.

### Testes

```powershell
uv run pytest tests/unit
```

### Frontend

```powershell
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Disponível em `http://localhost:3000`.

### Tudo via Docker Compose

```powershell
docker compose up --build
```

## Time

_Preencher com os nomes/integrantes do grupo (ver `docs/plano-de-trabalho.pdf`)._
