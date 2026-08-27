# Simple Todo — FastAPI

API de lista de tarefas (todos) construída com **FastAPI**, **SQLAlchemy 2 (async)** e
**Pydantic**, com autenticação via **JWT** e banco **PostgreSQL**. Projeto desenvolvido a
partir do curso [FastAPI do Zero](https://github.com/dunossauro) (ver
[Créditos](#-créditos-e-licença)).

## ✨ Funcionalidades

- Cadastro e gerenciamento de usuários (CRUD)
- Autenticação com **JWT** (login e refresh token) e senhas com hash **Argon2**
- CRUD de tarefas (todos) vinculadas ao usuário autenticado
- Listagem de tarefas com **filtros** (título, descrição, estado) e **paginação**
- Migrações de banco com **Alembic**
- Ambiente containerizado com **Docker Compose** (front + app + PostgreSQL)
- Atalhos de gerenciamento com **just**
- Suíte de testes com **pytest** (async) e cobertura 100%

## 🧰 Stack

| Camada       | Ferramenta                            |
| ------------ | ------------------------------------- |
| Web/API      | FastAPI                               |
| ORM          | SQLAlchemy 2 (async) + psycopg        |
| Banco        | PostgreSQL 16                         |
| Validação    | Pydantic / pydantic-settings          |
| Auth         | PyJWT + pwdlib (Argon2)               |
| Migrações    | Alembic                               |
| **Front-end**| **Nuxt 4 + TypeScript + Tailwind + Pinia** |
| Container    | Docker + Docker Compose               |
| Testes       | pytest, pytest-asyncio, factory-boy   |
| Lint/Format  | Ruff                                  |
| Task runner  | Taskipy / just                        |

## 🖥️ Front-end (painel "Andon")

Uma SPA/SSR em **Nuxt 4** (pasta [`frontend/`](frontend/)) que consome esta API.
A interface é um **painel de controle industrial**: cada tarefa é uma placa com
uma **lâmpada de estado** (rascunho / a fazer / fazendo / concluída / descarte).

Segurança de nível produto: o front usa um **BFF** (server routes do Nuxt) que
guarda o token JWT num cookie **httpOnly** (fora do JavaScript) e faz o *refresh*
de forma transparente. Como o navegador só fala com o próprio Nuxt, **não é
preciso configurar CORS** no FastAPI. Telas: login, cadastro, painel de tarefas
(CRUD + filtros + estados) e conta. Detalhes do sistema visual em
[`frontend/DESIGN.md`](frontend/DESIGN.md).

## 🚀 Instalação e execução (Docker + `just`)

A stack inteira — **front-end, API e banco** — sobe em containers. A única
ferramenta de operação necessária é o **`just`**: nada de instalar Node, Python
ou Poetry na máquina.

**Pré-requisitos:** [Docker](https://docs.docker.com/get-docker/) +
[Docker Compose](https://docs.docker.com/compose/) e
[just](https://github.com/casey/just).

```bash
git clone https://github.com/<seu-usuario>/simpleTodo_fastAPI.git
cd simpleTodo_fastAPI
cp .env.example .env   # opcional: ajuste as variáveis
just create            # build + sobe TUDO (front + app + banco)
```

Pronto. Sobem três serviços:

- 🖥️  **Front-end (painel):** http://localhost:3000
- 🔌  **API:** http://localhost:8000 (docs em `/docs`)
- 🐘  **PostgreSQL:** porta 5432

As migrações do Alembic rodam **automaticamente** ao subir a API
(`entrypoint.sh`). Depois de criado, gerencie tudo com um único comando:

| Comando       | Ação                                                         |
| ------------- | ------------------------------------------------------------ |
| `just create` | **Instalação:** build das imagens + cria e sobe os containers |
| `just start`  | Sobe os containers já criados (front + app + banco) juntos   |
| `just stop`   | Para os containers (sem removê-los)                          |
| `just down`   | Remove containers e rede (mantém o volume do banco)          |
| `just logs`   | Acompanha os logs da aplicação                               |
| `just status` | Mostra o status dos containers                               |

> Os dados do PostgreSQL persistem no volume `pgdata`, sobrevivendo a
> `stop`/`start` e `down`. Para apagar tudo, remova o volume:
> `docker compose down -v`.
>
> As seções abaixo (Poetry, migrações locais, etc.) são **opcionais** — só
> valem para desenvolver o back-end fora do Docker.

## 📋 Pré-requisitos (execução local, sem Docker)

- **Python 3.12+**
- **[Poetry](https://python-poetry.org/docs/#installation)** para gerenciamento de dependências
- Um **PostgreSQL** acessível (por exemplo, o do `docker compose`, exposto em `localhost:5432`)

## 🚀 Instalação local do back-end (opcional, sem Docker)

> Só é necessário se você quiser rodar o back-end fora do Docker. Para uso
> normal, o `just create` acima já resolve tudo.

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/simpleTodo_fastAPI.git
cd simpleTodo_fastAPI

# 2. Instale as dependências (cria o virtualenv automaticamente)
poetry install

# 3. Crie o arquivo de variáveis de ambiente
cp .env.example .env
```

### Variáveis de ambiente

O arquivo `.env` é lido por `simple_todo/settings.py`:

| Variável                      | Descrição                                | Exemplo                                                  |
| ----------------------------- | ---------------------------------------- | -------------------------------------------------------- |
| `DATABASE_URL`                | URL de conexão do banco                  | `postgresql+psycopg://app:app@localhost:5432/simple_todo` |
| `SECRET_KEY`                  | Chave usada para assinar os tokens JWT   | `secret_key`                                             |
| `ALGORITHM`                   | Algoritmo de assinatura do JWT           | `HS256`                                                  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do access token (em minutos)    | `30`                                                     |
| `POSTGRES_USER`               | Usuário do container PostgreSQL          | `app`                                                    |
| `POSTGRES_PASSWORD`           | Senha do container PostgreSQL            | `app`                                                    |
| `POSTGRES_DB`                 | Nome do banco do container PostgreSQL    | `simple_todo`                                            |

> ⚠️ **Importante:** o projeto usa engine assíncrona (`create_async_engine`), então o
> `DATABASE_URL` precisa de um driver async — para PostgreSQL use o prefixo
> `postgresql+psycopg://`. As variáveis `POSTGRES_*` são consumidas pelo `docker-compose`
> para provisionar o banco. Em produção, defina uma `SECRET_KEY` forte e única.

## 🗄️ Banco de dados (migrações)

> Com Docker, as migrações rodam **automaticamente** ao subir o container
> (`entrypoint.sh` executa `alembic upgrade head`). Os passos abaixo são para execução
> local sem Docker.

Aplique as migrações antes de subir a aplicação:

```bash
poetry run alembic upgrade head
```

Para criar uma nova migração após alterar os modelos:

```bash
poetry run alembic revision --autogenerate -m "descricao da mudanca"
```

## ▶️ Executando localmente (sem Docker)

```bash
# Modo desenvolvimento (com reload)
poetry run task run
```

O atalho `task run` executa `fastapi dev simple_todo/app.py`. A API sobe em:

- **API:** http://127.0.0.1:8000
- **Docs (Swagger):** http://127.0.0.1:8000/docs
- **Docs (ReDoc):** http://127.0.0.1:8000/redoc

## 🧪 Testes

```bash
# Roda lint + testes com cobertura (pre_test executa o lint automaticamente)
poetry run task test

# Formata o código e depois roda os testes
poetry run task testAll

# Gera o relatório HTML de cobertura em htmlcov/ (executado após 'task test')
poetry run task post_test
```

Para rodar o pytest diretamente (ou um arquivo/teste específico):

```bash
poetry run pytest
poetry run pytest tests/test_todo.py -q
```

## 🎨 Qualidade de código

```bash
poetry run task lint          # verifica com Ruff
poetry run task pre_format    # corrige problemas automaticamente (ruff check --fix)
poetry run task format        # formata o código (ruff format)
```

## 📡 Endpoints principais

| Método   | Rota                  | Descrição                             | Auth |
| -------- | --------------------- | ------------------------------------- | :--: |
| `GET`    | `/`                   | Health check                          |  —   |
| `POST`   | `/auth/token`         | Login — retorna access token          |  —   |
| `POST`   | `/auth/refresh_token` | Renova o access token                 |  ✅  |
| `POST`   | `/users/`             | Cria usuário                          |  —   |
| `GET`    | `/users/`             | Lista usuários                        |  —   |
| `GET`    | `/users/{user_id}`    | Detalha um usuário                    |  —   |
| `PUT`    | `/users/{user_id}`    | Atualiza usuário                      |  ✅  |
| `DELETE` | `/users/{user_id}`    | Remove usuário                        |  ✅  |
| `POST`   | `/todo/`              | Cria uma tarefa                       |  ✅  |
| `GET`    | `/todo/`              | Lista tarefas (filtros + paginação)   |  ✅  |
| `PATCH`  | `/todo/{todo_id}`     | Atualiza parcialmente uma tarefa      |  ✅  |
| `DELETE` | `/todo/{todo_id}`     | Remove uma tarefa                     |  ✅  |

### Filtros da listagem de tarefas (`GET /todo/`)

| Parâmetro     | Tipo   | Descrição                                            |
| ------------- | ------ | ---------------------------------------------------- |
| `title`       | str    | Filtra por título (busca parcial, 3–20 caracteres)   |
| `description` | str    | Filtra por descrição (busca parcial)                 |
| `state`       | enum   | `draft`, `todo`, `doing`, `done`, `trash`            |
| `offset`      | int    | Deslocamento para paginação (padrão `0`)             |
| `limit`       | int    | Quantidade máxima de itens (padrão `10`)             |

Exemplo:

```bash
curl -H "Authorization: Bearer <TOKEN>" \
  "http://127.0.0.1:8000/todo/?state=doing&limit=5"
```

### Atualização parcial de tarefa (`PATCH /todo/{todo_id}`)

Diferente de um `PUT`, o `PATCH` aceita apenas os campos a serem alterados
(`title`, `description` e/ou `state`) — os demais permanecem inalterados.

```bash
curl -X PATCH -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"state": "done"}' \
  "http://127.0.0.1:8000/todo/1"
```

## 🗂️ Estrutura do projeto

```
simple_todo/
├── app.py            # instancia o FastAPI e registra os routers
├── database.py       # engine e sessão async do SQLAlchemy
├── security.py       # hash de senha e JWT
├── settings.py       # configurações via .env
├── models/           # modelos ORM (pacote)
│   ├── __init__.py   # reexporta table_registry, User, Todo, TodoState
│   ├── registry.py   # registry() compartilhado pelos modelos
│   ├── user.py       # modelo User
│   └── todo.py       # modelo Todo + enum TodoState
├── schemas/          # schemas Pydantic (pacote)
│   ├── __init__.py   # reexporta todos os schemas
│   ├── base.py       # schemas comuns (Message, Token, FilterPage)
│   ├── user.py       # schemas de usuário (UserSchema, UserPublic, UserDB)
│   └── todo.py       # schemas de tarefa (TodoSchema, TodoPublic, TodoList,
│                     #                     TodoUpdate, FilterTodo)
└── routes/
    ├── auth.py       # /auth
    ├── users.py      # /users
    └── todo.py       # /todo
frontend/             # painel Nuxt 4 (SPA/SSR) — consome a API via BFF
├── app/              # pages, components, stores, layouts, composables
├── server/           # rotas BFF (auth httpOnly + proxy autenticado)
├── Dockerfile        # imagem do front-end (Node 22)
└── DESIGN.md         # sistema visual do painel "Andon"
tests/                # suíte de testes (pytest)
migrations/           # migrações do Alembic
Dockerfile            # imagem da aplicação (API)
docker-compose.yml    # orquestração (front + app + PostgreSQL)
entrypoint.sh         # roda as migrações e sobe a API no container
Justfile              # atalhos de gerenciamento (just create/start/stop)
```

## 🙏 Créditos e Licença

Baseado no material do curso **FastAPI do Zero**, originalmente escrito e produzido por
**Eduardo Mendes** ([@dunossauro](https://github.com/dunossauro)).

Todo o material do curso é gratuito e licenciado sob **Creative Commons
Atribuição-NãoComercial-CompartilhaIgual (CC BY-NC-SA)**:

- ✅ **Compartilhar:** copiar e redistribuir em qualquer suporte ou formato.
- ✅ **Adaptar:** remixar, transformar e criar a partir do material.
- ⚠️ **Atribuição:** dê o crédito apropriado ao criador original (Eduardo Mendes).
- 🚫 **Não Comercial:** não use o material para fins comerciais.
- 🔄 **CompartilhaIgual:** adaptações devem usar a mesma licença.

Leia o [LICENSE](LICENSE) ou a
[página oficial da licença](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt_BR).
