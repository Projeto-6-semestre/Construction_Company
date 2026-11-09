# Como começar — guia rápido pro time

Este arquivo é o passo a passo pra qualquer pessoa do time sair do zero até rodar o projeto na própria máquina e começar a trabalhar na sua tarefa. Dúvidas de workflow (Git, PR, deploy) estão em [`GUIA_PROJETO.md`](./GUIA_PROJETO.md); status atual do projeto está em [`README.md`](./README.md).

## 0. Pré-requisito: acesso ao repositório

O repositório é **privado**. Se você ainda não recebeu um convite por e-mail/notificação do GitHub pra entrar na organização `Projeto-6-semestre`, avise o responsável de infra antes de continuar — sem isso nenhum passo abaixo funciona.

## 1. Instalar o Git e configurar

1. Baixe em [git-scm.com/downloads](https://git-scm.com/downloads)
2. No terminal (PowerShell, Git Bash ou o terminal do VSCode), rode uma vez só:
   ```
   git config --global user.name "Seu Nome"
   git config --global user.email "seu-email-do-github@exemplo.com"
   ```

## 2. Clonar o projeto

```
git clone https://github.com/Projeto-6-semestre/Construction_Company.git
cd Construction_Company
```
Na primeira vez vai pedir login do GitHub — use seu usuário/senha ou token de acesso.

## 3. Abrir sua tarefa

Cada pessoa do time tem uma **issue no GitHub** com o que é responsabilidade dela (pastas, por onde começar, checklist). Veja a aba **"Issues"** do repositório no navegador, abra a que tem seu nome no título, e leia antes de mexer em qualquer coisa.

## 4. Instalar o que sua parte precisa

Nem todo mundo precisa instalar tudo — só o que a sua tarefa usa:

| Se sua tarefa é... | Você precisa de | Onde tem o passo a passo |
|---|---|---|
| Back-end, banco de dados ou QA | Python 3.12+, `uv`, Docker Desktop | `README.md`, seção "Backend" |
| Front-end ou QA | Node.js 20+, `npm` | `README.md`, seção "Frontend" |
| Documentação (ABNT ou apoio) | Nada além do Git — edita `.md`/`.pdf` direto | — |

Depois de instalado, siga o `README.md` → **"Como rodar localmente"** pra subir o back-end, o banco e/ou o front-end.

## 5. Trabalhar na tarefa (fluxo de toda vez)

```
git checkout main
git pull origin main
git checkout -b feature/nome-curto-da-sua-tarefa
```

Faça as mudanças, teste local, e:

```
git add .
git commit -m "mensagem clara do que foi feito"
git push origin feature/nome-curto-da-sua-tarefa
```

No GitHub, abra o **Pull Request** (aparece um botão assim que o push termina). Na descrição, escreva `Closes #N` trocando `N` pelo número da sua issue — isso fecha a issue automaticamente quando o PR for aprovado e mergeado.

**Nunca** dá push direto na `main` — sempre passa por branch + Pull Request + revisão de alguém do time (ver seção 2 e 3 do `GUIA_PROJETO.md`).

## 6. Travou em algo?

Comenta na sua própria issue no GitHub descrevendo o problema — fica registrado ali pro time todo ver, em vez de se perder numa conversa de WhatsApp.
