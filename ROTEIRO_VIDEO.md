# Roteiro do vídeo de apresentação

Roteiro pra quem for gravar sozinho explicando o projeto — não é texto pra decorar palavra por palavra, são os pontos a cobrir em cada parte, com uma sugestão de fala pros momentos-chave (abertura e fechamento). Duração estimada: **7-9 minutos**.

Antes de gravar: tenha abertas as abas do **painel interno** (logado), da **loja pública**, do **Swagger** (`/docs` do back-end) e o **VSCode** com o projeto.

---

## 1. Abertura (até 1 min)

Fala sugerida:

> "Oi, eu sou o Eduardo Daniel, e esse é o projeto [nome do grupo/projeto] — um sistema de controle de estoque com agente de inteligência artificial, feito pra uma empresa de materiais de construção. Nesse vídeo eu vou mostrar como ele funciona na prática, a arquitetura por trás, e provar que está rodando de verdade na internet, não só local."

- Diga o nome da disciplina/projeto de extensão e a faculdade, se for pedido no enunciado da professora.
- Uma frase sobre o problema que o projeto resolve: "hoje muita loja de material de construção não tem controle de estoque em tempo real — aqui, toda entrada e saída passa pelo sistema, então o número que aparece é sempre o real."

## 2. A ideia do projeto (1-2 min)

Cobrir, sem precisar decorar:

- **Quem usa**: dois públicos — o **cliente final** (compra na loja pública) e a **equipe interna** (gerencia estoque, vê pedidos, usa o agente de IA).
- **O diferencial**: um agente de IA que conversa em linguagem natural pra consultar estoque e registrar pedidos — mas ele **nunca** gera código/SQL livre, só escolhe entre um conjunto fixo de ferramentas seguras (mencione isso, é um ponto técnico forte pra mostrar maturidade de projeto).
- **Fluxo de venda real**: cliente monta carrinho na loja → finaliza → pedido grava no banco **e** abre o WhatsApp da empresa com o resumo pronto, pra combinar pagamento/entrega (mesma lógica de site de pizzaria/delivery pequeno).

## 3. Demonstração ao vivo — loja pública (2 min)

Na aba da loja (`/loja`):

1. Mostre o catálogo, filtro por categoria.
2. Adicione 1-2 produtos ao carrinho.
3. Preencha o nome e clique em "Finalizar pedido".
4. Mostre o WhatsApp abrindo com a mensagem pronta (não precisa enviar de verdade).

## 4. Demonstração ao vivo — painel interno (3 min)

Na aba do painel (já logado):

1. **Tela inicial**: estoque + chat com o agente de IA. Pergunte algo tipo *"qual o estoque de cimento?"* ou *"quais produtos estão abaixo do mínimo?"* ao vivo, mostrando a resposta da IA.
2. **Gerenciar produtos**: mostre o cadastro/edição de um produto.
3. **Pedidos**: mostre o pedido que você acabou de fazer na loja aparecendo aqui — "a equipe vê exatamente o que o cliente pediu".
4. **Dashboard**: mostre os cards de entrada/saída e o gráfico por categoria — "isso dá uma noção financeira de quanto entrou e saiu, pra equipe fazer as contas".

## 5. Por trás dos panos — arquitetura e código (2 min)

Troque pro VSCode. Não precisa ler código linha a linha, só mostrar a organização:

- **Duas pastas separadas**: `app/` (back-end, Python/FastAPI) e `frontend/` (front-end, Next.js/React) — linguagens diferentes, conversando só por API HTTP.
- Dentro do back-end, abra rapidamente `app/api`, `app/services`, `app/repositories`, `app/models`, `app/agent` e diga uma frase de cada: "rotas aqui, regra de negócio aqui, acesso ao banco aqui, tabelas aqui, o agente de IA aqui — cada camada só faz uma coisa, isso facilita manutenção e deixa o projeto dividido entre a equipe sem um atropelar o outro".
- Mostre rapidamente que o código **tem comentários explicando o porquê** das decisões (abra 1 arquivo de exemplo).
- Mencione: testes automatizados (`pytest`), CI rodando a cada push no GitHub.

## 6. Provando que está no ar (1-2 min)

- Abra a URL da **Vercel** (front-end) direto no navegador, sem estar logado no VSCode/local — "isso é a internet de verdade, não é `localhost`".
- Abra a URL do **Render** + `/docs` (Swagger do back-end) — mostre as rotas documentadas automaticamente.
- Uma frase sobre a stack de hospedagem: "front-end na Vercel, back-end no Render, banco de dados PostgreSQL no Neon — tudo gratuito, pensado pra um projeto acadêmico".

## 7. Fechamento (30s)

Fala sugerida:

> "Resumindo: um sistema completo, com loja pública, painel interno, agente de IA, dashboard, e rodando de verdade na internet — não é só um protótipo local. Obrigado!"

- Se for pedido, cite os integrantes do grupo e o papel de cada um.

---

## Checklist antes de gravar

- [ ] Banco (Neon) com produtos cadastrados (não vazio) — senão a demo fica sem graça
- [ ] Testar o fluxo de pedido → WhatsApp uma vez antes de gravar, pra não travar ao vivo
- [ ] Fechar abas/notificações desnecessárias (e-mail, WhatsApp pessoal) antes de compartilhar tela
- [ ] Decidir se vai editar depois (cortar silêncios) ou gravar em uma tomada só
