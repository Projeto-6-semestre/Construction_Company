# CLAUDE.md — Guia de Workflow do Projeto

> **Status:** rascunho v0.1 — construído a partir dos guias internos (`docs servico/`) e da análise do projeto de referência `wmsbox-agent`. Ainda precisa ser validado e ajustado pelo time antes de virar regra definitiva. Este arquivo é vivo: sempre que o time decidir algo novo (ou mudar de ideia), atualiza aqui.
>
> **Stack do projeto:** Python + RAG (inspirado no `wmsbox-agent`, mas evoluindo bem além dele — ver seção 9).
> **Organização GitHub:** `Projeto-6-semestre` (repositório privado).
> **Quem sobe código:** o time, manualmente. Claude Code não faz commit/push/deploy — só ajuda a planejar, documentar e (quando pedido) escrever código local.

---

## 1. Papel deste documento

Este é o documento de referência que qualquer pessoa do time (ou o Claude Code, quando estiver ajudando alguém do time) deve consultar para saber **como trabalhamos aqui**: como o Git/GitHub está organizado, como fazemos deploy, como lidamos com migrations de banco, e qual a ordem de passos até o primeiro deploy no ar.

As ideias aqui vieram de projetos reais anteriores (WMS PRO e chat_ia, documentados em `docs servico/`), adaptadas de Node/PHP para **Python**, e da análise crítica do `wmsbox-agent` (o que ele faz bem, e principalmente o que faltava nele e vamos evitar repetir.

---

## 2. Organização do repositório no GitHub

- Repositório vive dentro da **organização** `Projeto-6-semestre`, nunca em conta pessoal — isso protege o projeto de depender de uma única pessoa (se alguém sair do grupo, o repo continua acessível para o resto do time).
- Visibilidade: **privado**.
- **Antes do primeiro commit**: rodar uma auditoria rápida procurando segredos/chaves hardcoded no código (tokens de API de LLM, senhas, etc.). Uma vez que algo entra no histórico do Git, fica lá "pra sempre" mesmo se for apagado depois — então essa checagem é antes de existir histórico, não depois.
- `.gitignore` robusto desde o **commit zero**, cobrindo pelo menos:
  ```
  .env
  .env.*
  !.env.example
  __pycache__/
  *.pyc
  .venv/
  venv/
  *.egg-info/
  .pytest_cache/
  .mypy_cache/
  .ruff_cache/
  data/uploads/          # se o RAG aceitar upload de documentos
  *.db
  *.sqlite3
  credentials/
  !credentials/.gitkeep
  ```
- Manter um `.env.example` **sem valores reais** sempre versionado, espelhando todas as variáveis que o `.env` real precisa ter.
- Permissões: quem efetivamente desenvolve tem role **Write**. Se algum dia existir conta institucional/compartilhada (bot de deploy, por ex.), ela fica como **Read** — nunca comita, só para preservar rastreabilidade de quem fez o quê.
- **Branch protection na `main`**: ativar "Require a pull request before merging" + pelo menos 1 aprovação.
  - ⚠️ **Ressalva importante**: em repositório **privado** dentro de uma organização no plano **gratuito** do GitHub, essa trava fica salva na configuração mas **não é tecnicamente reforçada** (isso exige o plano Team pago). Ou seja, hoje isso funciona como **combinado de honra do time**, não como bloqueio técnico. Se o projeto crescer/virar algo sério, avaliar upgrade de plano.
- Nunca push direto na `main`. Sempre: branch → PR → revisão de alguém do time → merge.

---

## 3. Fluxo de trabalho no dia a dia

```
git checkout main
git pull origin main
git checkout -b feature/nome-da-feature      # ou fix/..., hotfix/...

# desenvolver, testar local

git add .
git commit -m "mensagem clara"
git push origin feature/nome-da-feature

# abrir Pull Request no GitHub
# pelo menos 1 colega revisa e aprova
# se a PR incluir migration de banco, mencionar isso na descrição da PR

# merge na main
```

Convenção de nome de branch sugerida: `feature/...`, `fix/...`, `hotfix/...`, `chore/...`.

Regras inegociáveis (repetidas em todos os guias que lemos, valem para qualquer stack):
- Nunca testar direto em produção.
- Fluxo sempre: **local → homologação/staging → produção**.
- Nunca commitar `.env` ou qualquer arquivo com segredo real.
- Nunca compartilhar chave SSH ou token do GitHub fora dos campos de *Secret* do próprio GitHub.
- Avisar o time antes de qualquer deploy em produção.
- Checar logs depois de todo deploy.

---

## 4. Arquitetura do projeto (camadas / "MVC" adaptado para Python + RAG)

O `wmsbox-agent` (projeto de inspiração) **não tem** separação em camadas — é um script único onde config, dado e lógica de negócio se misturam, o que dificulta testar e crescer. Vamos evitar isso desde o início.

Estrutura de pastas já criada no repositório (esqueleto, sem código ainda — cada pasta tem um `.gitkeep`):

```
app/
├── api/            # camada de apresentação: rotas/endpoints (ex: FastAPI routers)
├── services/       # lógica de negócio / orquestração (equivalente ao "controller" do MVC)
├── models/         # modelos de banco (ORM) + schemas de validação (Pydantic)
├── repositories/   # acesso a dados (camada entre services e banco/models)
├── rag/
│   ├── ingestion/  # carregamento e chunking de documentos
│   ├── embeddings/ # geração de embeddings
│   └── retrieval/  # busca vetorial / re-ranking / montagem de contexto
├── core/           # config tipada, segurança, logging — sem depender de framework de apresentação
migrations/          # migrations de banco (Alembic — ver seção 6)
tests/
├── unit/
└── integration/
scripts/             # scripts utilitários (seed de dados, manutenção, etc.)
docs/                # documentação adicional do projeto
```

Princípios (tirados do "prompt de auditoria de segurança MVC" e do que faltou no `wmsbox-agent`):
- Ponto único de entrada da aplicação.
- Sem lógica de negócio duplicada espalhada entre camadas.
- `core/config.py` (configuração) não deve importar nada de apresentação (o `wmsbox-agent` tinha `import streamlit` dentro do config — evitar esse acoplamento).
- Nada de efeito colateral pesado no `import` de módulo (o `wmsbox-agent` carregava o CSV e criava o agente já ao importar o módulo — dificulta testes unitários). Inicialização explícita (factory functions), não implícita.
- Configuração de ambiente **tipada e validada** (ex: `pydantic-settings`), não só variáveis soltas lidas com `os.getenv` espalhadas pelo código.

**A definir com o time** (ideias/sugestões, não decisão fechada):
- Framework web: FastAPI (assíncrono, docs automáticas, tipagem nativa com Pydantic) é o mais indicado para uma API Python moderna.
- ORM + migrations: SQLAlchemy 2.x + Alembic.
- Empacotamento/dependências: `pyproject.toml` + lockfile (Poetry ou `uv`) em vez de só `requirements.txt` com `>=` solto (foi um ponto fraco identificado no projeto de referência — sem pin exato, builds diferentes em máquinas diferentes do time podem se comportar diferente).
- Lint/format: `ruff` (lint + format).
- Testes: `pytest`.

---

## 5. GitHub Actions / CI-CD

### 5.1 Ambientes

Seguindo o padrão observado nos dois projetos reais que analisamos, usar **3 ambientes**:

| Ambiente | Propósito | Deploy |
|---|---|---|
| Local | Máquina de cada dev | manual, `docker run` / rodar direto |
| Homologação (staging) | Validar antes de ir pra produção | **automático** a cada merge na `main` |
| Produção | Ambiente real | **manual**, disparado via `workflow_dispatch` com confirmação explícita |

### 5.2 Workflows sugeridos

**`deploy-homologacao.yml`** — dispara em todo push/merge na `main`:
```yaml
name: Deploy Homologação
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint & testes
        run: |
          pip install -r requirements.txt
          ruff check .
          pytest
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd ${{ secrets.VPS_PATH_HOMOLOGACAO }}
            git pull origin main
            # migration entra aqui SOMENTE se o time decidir automatizar (ver seção 6.3)
            docker compose up -d --build
```

**`deploy-producao.yml`** — manual, com confirmação obrigatória (evita deploy acidental):
```yaml
name: Deploy Produção
on:
  workflow_dispatch:
    inputs:
      confirmacao:
        description: 'Digite CONFIRMAR para prosseguir'
        required: true
jobs:
  checar_confirmacao:
    runs-on: ubuntu-latest
    steps:
      - name: Validar palavra de confirmação
        run: |
          if [ "${{ github.event.inputs.confirmacao }}" != "CONFIRMAR" ]; then
            echo "Confirmação inválida, abortando."
            exit 1
          fi
  deploy:
    needs: checar_confirmacao
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd ${{ secrets.VPS_PATH_PRODUCAO }}
            git pull origin main
            docker compose up -d --build
```

> Estes YAMLs são **exemplo/referência** para o time escrever o real junto — não foram criados como arquivo `.github/workflows/*.yml` no projeto ainda, por decisão consciente (quem sobe/configura isso no repositório é o time, manualmente).

### 5.3 Secrets necessários (GitHub → Settings → Secrets and variables → Actions)

- `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` (chave SSH **dedicada** ao deploy, gerada só pra isso: `ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N ""` — nunca reaproveitar chave pessoal).
- `VPS_PATH_HOMOLOGACAO`, `VPS_PATH_PRODUCAO`.
- Chaves de API do(s) provedor(es) de LLM usados no RAG (ex: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `HUGGINGFACE_API_TOKEN` — o que o time decidir usar).
- ⚠️ Se **Deploy Keys** (SSH) do GitHub estiverem desativadas por política da organização (aconteceu num dos projetos de referência, erro HTTP 422), a alternativa é clonar via **Personal Access Token** na URL (`https://usuario:TOKEN@github.com/...`), de preferência gerado numa conta institucional, não pessoal. A chave SSH que o Actions usa pra conectar no VPS é um mecanismo diferente e não é afetada por essa política.

---

## 6. Migrations de banco de dados

O `wmsbox-agent` não tem banco de dados (só um CSV estático), então isso é **greenfield total** — mas os projetos de referência (Node/Sequelize e PHP) deixaram práticas valiosas para adaptar:

### 6.1 Ferramenta

**Alembic** (o "Sequelize CLI" do mundo Python/SQLAlchemy). Convenção:
- Cada migration tem `upgrade()` e `downgrade()` — `downgrade()` deve desfazer **exatamente** o que `upgrade()` fez.
- Nome de migration descritivo (Alembic já prefixa com revisão/ordem).
- **Migration e o Model correspondente sempre no mesmo commit / mesma PR** — quem revisa vê a estrutura de banco junto com o código que depende dela. A descrição da PR deve citar quais migrations estão incluídas.

### 6.2 Checklist antes de abrir PR com migration

- [ ] Rodou local sem erro?
- [ ] Conferiu a estrutura resultante no banco?
- [ ] `downgrade()` desfaz exatamente o que o `upgrade()` fez?
- [ ] Migration commitada junto com o código/model que depende dela?
- [ ] PR menciona as migrations incluídas?
- [ ] No roteiro de deploy, o `migrate` está posicionado **antes** do restart da aplicação?

### 6.3 Automática vs. manual — decisão que o time precisa tomar conscientemente

Os dois projetos de referência tomaram decisões **opostas**, e ambas são válidas dependendo do apetite a risco:
- **Automática dentro do próprio workflow de deploy** (mais ágil, mais risco) — migration roda sozinha a cada deploy.
- **Manual e deliberada**, comando separado rodado por uma pessoa (mais lenta, mais segura) — usada quando o time quer controle explícito sobre mudanças de banco em produção.

> **Sugestão inicial para este projeto**: começar com migration **manual** em produção (comando explícito, não dentro do workflow automático) até o time ganhar confiança no processo — e automatizar depois se fizer sentido. Ajustar aqui quando decidido.

### 6.4 Regra crítica de ordem

`migrate` roda **sempre antes** do restart/reload da aplicação — o código novo pode referenciar colunas que ainda não existem se a ordem for invertida.

### 6.5 Se der errado

Se uma migration falhar em produção, o banco fica no estado anterior (nada corrompido). Reverter com `alembic downgrade -1`, corrigir, abrir novo PR.

---

## 7. Processo de deploy

### 7.1 Setup único de infraestrutura (feito uma vez)

1. Provisionar VPS (ou usar free tier de nuvem, ex: Oracle Cloud Always Free — foi o que o `wmsbox-agent` usou).
2. Instalar Docker + Docker Compose.
3. Configurar firewall: abrir só 22 (SSH), 80 (HTTP), 443 (HTTPS); bloquear acesso direto às portas internas da app/banco.
4. Instalar Nginx como **proxy reverso** (testar com `nginx -t` antes de recarregar, nunca derrubar o serviço direto).
5. Subir banco de dados (container) e rodar migrations iniciais.
6. Clonar o repositório no servidor (via token ou Deploy Key), em pasta própria por ambiente.
7. Criar `.env` real no servidor a partir do `.env.example` (nunca versionado).
8. Configurar DNS (registro A) se houver domínio.
9. Emitir certificado HTTPS via Certbot, com renovação automática.
10. Repetir 4-9 para o ambiente de **homologação**, em pasta/porta/subdomínio próprios.
11. Configurar Secrets no GitHub (seção 5.3) e branch protection (seção 2).
12. Criar os workflows de deploy (seção 5.2).
13. Validar bem antes de desligar qualquer infraestrutura antiga (zero downtime).

### 7.2 Fluxo do dia a dia

1. PR aprovado e mergeado na `main`.
2. **Deploy automático em homologação** dispara (Actions → SSH no VPS → pull → migrate se a política permitir → `docker compose up -d --build`).
3. Testar manualmente em homologação. Se algo estiver errado, corrigir e repetir — nunca promover bug conhecido para produção.
4. **Deploy manual em produção**: rodar o workflow no GitHub Actions, digitar a palavra de confirmação exata, avisar o time antes.
5. Verificar logs após o deploy.

### 7.3 Dockerfile (referência/ideia, ainda a escrever pelo time)

O `wmsbox-agent` tem um Dockerfile simples que já acerta o básico (copiar `requirements.txt` antes do código pra aproveitar cache de camada):
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Diferente do projeto de referência, o novo projeto deve ter `docker-compose.yml` (app + banco + o que mais precisar), já que teremos banco de dados real.

---

## 8. Segurança — checklist (adaptado do prompt de auditoria MVC, para Python/RAG)

- **Segredos**: nunca hardcoded; sempre via `.env`/Secrets; `.env.example` sem valores reais.
- **Autenticação**: hashing de senha com biblioteca própria pra isso (ex: `passlib`/`bcrypt`), nunca hash fraco puro; ID do usuário sempre vindo de sessão/token, nunca de parâmetro solto na URL.
- **Controle de acesso (IDOR)**: toda rota que busca recurso por ID valida que o usuário tem permissão sobre aquele dado.
- **Injeção**: sempre usar ORM/queries parametrizadas, nunca montar SQL por concatenação de string.
- **Execução de código gerado por LLM** — ponto de atenção **específico de RAG/agentes**: o `wmsbox-agent` usa `allow_dangerous_code=True` (executa código Python gerado pelo LLM sem sandbox) e reconhece isso como aceitável só porque era uso local — mas a versão pública dele (Streamlit Cloud) fica exposta a qualquer um. **Vamos evitar repetir isso**: se o agente gerar/executar código, avaliar sandboxing, allowlist de operações, ou validar a query antes de rodar.
- **Uploads** (se o RAG aceitar documentos): validar tipo por conteúdo real, renomear arquivo, guardar fora de pasta pública executável, limitar tamanho.
- **Config de ambiente**: separar claramente dev/staging/produção; modo debug desligado em produção; logs nunca gravam segredos.
- **Dependências**: usar lockfile, revisar versões desatualizadas/CVEs periodicamente.
- **Headers/HTTPS**: CORS restrito (nunca `*` com credenciais), CSRF em formulários que alteram dado, HTTPS forçado em produção.

---

## 9. O que aprendemos com o `wmsbox-agent` (projeto de inspiração) — o que vamos fazer diferente

O `wmsbox-agent` é um protótipo didático simples (agente de dados tabulares via LangChain + pandas sobre um CSV, não um RAG documental de verdade). Pontos que vamos melhorar no novo projeto:

1. **Sem testes automatizados lá** → aqui: `pytest` desde o início, com testes de unidade e (quando fizer sentido) eval sets pra respostas do LLM.
2. **Sem CI/CD lá** (deploy 100% manual via SSH, documentado passo a passo) → aqui: Actions rodando lint/test em toda PR, e deploy automatizado em homologação (seção 5).
3. **`allow_dangerous_code=True` sem sandbox** → aqui: avaliar sandboxing/allowlist antes de expor qualquer execução de código gerado por LLM (seção 8).
4. **Dependência de `langchain-experimental`**, pacote sem manutenção ativa → aqui: evitar depender de peças "experimental" sem plano de vida longo para o núcleo do agente; isolar atrás de interface própria se for usar.
5. **Sem separação de camadas** (efeito colateral no import, config acoplada à apresentação) → aqui: arquitetura em camadas desde o início (seção 4).
6. **Nenhum vector store / RAG documental de verdade** (era só um DataFrame em memória) → aqui: se o objetivo for RAG sobre documentos, desenhar pipeline de ingestão → chunking → embeddings → vector store (Chroma/FAISS/pgvector, a decidir) → retrieval, do zero.
7. **Sem banco de dados/migrations** → aqui: banco real com Alembic desde cedo (seção 6).
8. **Config "single-file .env" sem validação de schema** → aqui: config tipada (`pydantic-settings`).
9. **Sem infraestrutura como código** (VPS configurado manualmente clicando em console) → aqui: pelo menos documentar/scriptar o setup (mesmo sem Terraform completo, ter um script/checklist reprodutível).
10. **`requirements.txt` sem lockfile** → aqui: `pyproject.toml` + lockfile.

---

## 10. Roadmap sugerido — por onde começar até o primeiro deploy

Ordem recomendada para o time (ajustável, mas é uma sequência lógica testada nos projetos de referência):

1. **Definir stack final** com o time (framework web, ORM, ferramenta de RAG/vector store) — ver sugestões na seção 4.
2. **Criar o repositório** na organização `Projeto-6-semestre` (privado) com `.gitignore` já robusto e `.env.example`.
3. **Primeira subida do código** (a estrutura de pastas que já está pronta aqui + um "hello world" mínimo da API).
4. **Configurar permissões da equipe** e branch protection na `main` (com a ressalva do plano gratuito, seção 2).
5. **Configurar banco de dados local** + Alembic com a primeira migration.
6. **Escrever o núcleo do RAG/agente** (camada `app/rag/`), testável isoladamente das camadas de apresentação.
7. **Expor a API** (`app/api/`) consumindo o serviço de RAG.
8. **Escrever testes** (unidade pelo menos para `services/` e `rag/`).
9. **Provisionar VPS** e instalar Docker/Nginx/Certbot.
10. **Escrever os workflows do GitHub Actions** (homologação automática, produção manual com confirmação) e configurar os Secrets.
11. **Primeiro deploy em homologação**, validar manualmente.
12. **Primeiro deploy em produção**, avisar o time, verificar logs, marco alcançado 🎯.

---

## 11. Pendências / decisões em aberto para o time discutir

- [ ] Nome definitivo do repositório.
- [ ] Framework web definitivo (sugestão: FastAPI).
- [ ] Vector store definitivo, se o RAG for documental (Chroma? FAISS? pgvector?).
- [ ] Provedor de LLM (Anthropic? OpenAI? outro?).
- [ ] Migration automática ou manual em produção (seção 6.3) — sugestão inicial: manual.
- [ ] Onde hospedar (VPS próprio? Oracle Cloud free tier como o projeto de referência? outro?).
- [ ] Regras adicionais de code review / convenção de commit que o time quiser formalizar aqui.
