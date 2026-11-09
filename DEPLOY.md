# Deploy gratuito — guia passo a passo

## Por que não é só "subir na Vercel"

A Vercel é feita pela mesma empresa do Next.js e é perfeita pro **front-end** — mas ela não hospeda bem o tipo de back-end que esse projeto tem (FastAPI com conexão persistente ao Postgres, Alembic, agente de IA). Pra ter o projeto completo rodando de graça na internet, a gente usa **3 serviços gratuitos diferentes**, cada um fazendo a parte que ele faz melhor:

| Parte | Serviço | Por quê |
|---|---|---|
| Front-end (Next.js) | **Vercel** | Feito pra isso, zero configuração |
| Back-end (FastAPI) | **Render** | Plano free roda Python de verdade (não é serverless) — ver [Render docs](https://render.com/docs/free) |
| Banco de dados (Postgres + pgvector) | **Neon** | Postgres gerenciado gratuito com pgvector já disponível — ver [Neon](https://neon.com) |

**Limitação do plano free do Render**: o serviço "dorme" depois de 15 minutos sem uso e demora ~1 minuto pra acordar na próxima requisição. Pra uma demonstração em sala de aula isso é tranquilo — só avise a pessoa que for mostrar que o primeiro load pode demorar um pouco.

Eu não consigo criar essas contas nem clicar nos dashboards por vocês — isso precisa ser feito por login de alguém do time em cada site. Preparei os arquivos de configuração (`render.yaml`) e esse guia; os passos abaixo são o que falta fazer manualmente.

## Ordem importa

Banco → Back-end → Front-end → voltar no Back-end pra liberar o CORS. Cada etapa usa uma informação gerada na etapa anterior.

---

### 1. Banco de dados (Neon)

1. Crie uma conta em [neon.com](https://neon.com) (dá pra logar com GitHub).
2. Crie um projeto novo, nome sugerido: `estoque-construcao`.
3. No painel do projeto, ative a extensão **pgvector** (geralmente é um toggle/SQL `CREATE EXTENSION vector;` direto no editor SQL do Neon).
4. Copie a **connection string** que o Neon fornece. Ela vem parecida com:
   ```
   postgresql://usuario:senha@ep-xxxxx.neon.tech/estoque_construcao?sslmode=require
   ```
5. **Ajuste pro formato que o projeto usa** (SQLAlchemy async + asyncpg) — troque `postgresql://` por `postgresql+asyncpg://` e `?sslmode=require` por `?ssl=require`:
   ```
   postgresql+asyncpg://usuario:senha@ep-xxxxx.neon.tech/estoque_construcao?ssl=require
   ```
   Guarde essa string — é o `DATABASE_URL` que vai no Render no próximo passo. Se a conexão falhar por causa do SSL, essa troca de parâmetro é o primeiro lugar pra conferir.

### 2. Back-end (Render)

1. Crie uma conta em [render.com](https://render.com) (login com GitHub facilita — ele já teria acesso ao repositório se a conta do GitHub usada for uma que já está na organização `Projeto-6-semestre`).
2. "New" → "Blueprint" → aponte pro repositório `Projeto-6-semestre/Construction_Company`. O Render vai ler o [`render.yaml`](./render.yaml) que já está na raiz do projeto e propor o serviço automaticamente.
3. Antes de confirmar, preencha as variáveis de ambiente marcadas como "a definir" (vêm do `render.yaml` sem valor, por segurança — nunca ficam no Git):
   - `DATABASE_URL` → a connection string do Neon (passo 1)
   - `GROQ_API_KEY` → sua chave da Groq (`console.groq.com/keys`)
   - `JWT_SECRET` → gere um valor aleatório próprio: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `CORS_ALLOW_ORIGINS` → por enquanto deixe um valor qualquer tipo `https://placeholder.vercel.app` (volta nesse passo depois)
4. Deploy. O `render.yaml` já manda rodar `alembic upgrade head` antes de subir a aplicação, então o banco é criado/atualizado automaticamente no primeiro deploy.
5. Quando terminar, copie a URL pública que o Render gera, algo como `https://estoque-construcao-api.onrender.com`.
6. **Criar o primeiro usuário do painel** (não existe cadastro público, de propósito): na sua máquina, edite seu `.env` local trocando temporariamente `DATABASE_URL` pela string do Neon, rode:
   ```
   uv run python scripts/criar_admin.py admin "sua-senha-aqui"
   ```
   e depois volte o `.env` pro valor local de novo.

### 3. Front-end (Vercel)

1. Crie uma conta em [vercel.com](https://vercel.com) (login com GitHub).
2. "Add New" → "Project" → importe o repositório `Projeto-6-semestre/Construction_Company`.
3. **Root Directory**: configure como `frontend` (o projeto Next.js não está na raiz do repositório, está em `frontend/`) — a Vercel pergunta isso na tela de configuração do projeto.
4. Em "Environment Variables", adicione:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://estoque-construcao-api.onrender.com
   ```
   (a URL do Render que você copiou no passo 2.5)
5. Deploy. A Vercel te dá uma URL tipo `https://construction-company.vercel.app`.

### 4. Voltar no Render e liberar o CORS

Sem isso o navegador bloqueia as chamadas do front-end pro back-end (erro de CORS no console).

1. No Render, vá em **Settings → Environment** do serviço do back-end.
2. Edite `CORS_ALLOW_ORIGINS` pra URL real da Vercel: `https://construction-company.vercel.app` (sem barra no final).
3. Salve — o Render reinicia o serviço sozinho com a variável nova.

---

## Depois do primeiro deploy

- Todo `git push` na branch conectada (geralmente `main`) faz **Render e Vercel re-deployarem sozinhos** — é esse o "CI/CD automático em homologação" que o [`GUIA_PROJETO.md`](./GUIA_PROJETO.md) (seção 5) descrevia, só que usando esses dois serviços em vez de VPS + GitHub Actions manual.
- Migrations novas: como o `preDeployCommand` do `render.yaml` já roda `alembic upgrade head` a cada deploy, qualquer migration nova commitada sobe sozinha — não precisa de passo manual (isso é diferente da sugestão original de "migration manual em produção" do `GUIA_PROJETO.md`, seção 6.3; optamos por automático aqui porque é um único ambiente de demonstração, não uma produção real com usuários pagantes).
- Se o banco do Neon ficar inativo por muito tempo sem uso, ele pode suspender o compute (volta sozinho na próxima conexão, mas pode demorar alguns segundos) — normal no plano free.
