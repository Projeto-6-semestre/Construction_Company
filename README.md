# Agente de Estoque — Materiais de Construção

> Agente de IA via chat para controle de estoque de uma empresa de materiais de construção (blocos, cimento, areia, ferramentas). O agente sempre sabe o número certo de estoque porque toda entrada/saída passa por ele — sem contagem manual.

## Fase atual: Fase 1 — Motor de estoque + chat (back-end e front-end funcionais)

- [x] Estrutura de pastas e `CLAUDE.md`
- [x] Repositório criado na organização GitHub
- [x] Stack definida: FastAPI + SQLAlchemy/Alembic + PostgreSQL (pgvector reservado) + Hugging Face + React/Next.js
- [x] Banco de dados + migration inicial (5 tabelas: produtos, fornecedores, pedidos, itens_pedido, movimentacoes_estoque)
- [x] Camada de serviço com regra de negócio (pedido só confirma se TODOS os itens tiverem estoque)
- [x] Agente de IA via LangChain (tool-calling, sem execução de código/SQL livre)
- [x] API FastAPI (`/health`, `/produtos`, `/pedidos`, `/chat`)
- [x] Frontend React/Next.js (chat + painel de estoque)
- [x] Testes unitários da camada de serviço (5/5 passando)
- [ ] Deploy em homologação

Roadmap completo em [`CLAUDE.md`](./CLAUDE.md), seção 10. Detalhes de papéis/responsabilidades em [`docs/plano-de-trabalho.pdf`](./docs/plano-de-trabalho.pdf).

## Stack

Python 3.12+ · FastAPI (async) · SQLAlchemy 2.x + Alembic · PostgreSQL (`pgvector/pgvector:pg16`) · LangChain + Hugging Face (`Qwen/Qwen2.5-72B-Instruct`) · React + Next.js · `uv` · pytest · Docker.

## Como rodar localmente

### Backend

```powershell
# 1. Instalar dependencias
uv sync

# 2. Copiar e preencher o .env (precisa de um token gratuito da Hugging Face)
cp .env.example .env
# edite .env e preencha HUGGINGFACE_API_TOKEN

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
