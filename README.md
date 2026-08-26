# Simple Todo — FastAPI

API de lista de tarefas (todos) construída com **FastAPI**, **SQLAlchemy 2 (async)** e
**Pydantic**, com autenticação via **JWT**. Projeto desenvolvido a partir do curso
[FastAPI do Zero](https://github.com/dunossauro) (ver [Créditos](#-créditos-e-licença)).

## ✨ Funcionalidades

- Cadastro e gerenciamento de usuários (CRUD)
- Autenticação com **JWT** (login e refresh token) e senhas com hash **Argon2**
- CRUD de tarefas (todos) vinculadas ao usuário autenticado
- Listagem de tarefas com **filtros** (título, descrição, estado) e **paginação**
- Migrações de banco com **Alembic**
- Suíte de testes com **pytest** (async) e cobertura 100%

## 🧰 Stack

| Camada       | Ferramenta                          |
| ------------ | ----------------------------------- |
| Web/API      | FastAPI                             |
| ORM          | SQLAlchemy 2 (async) + aiosqlite    |
| Validação    | Pydantic / pydantic-settings        |
| Auth         | PyJWT + pwdlib (Argon2)             |
| Migrações    | Alembic                             |
| Testes       | pytest, pytest-asyncio, factory-boy |
| Lint/Format  | Ruff                                |
| Task runner  | Taskipy                             |

## 📋 Pré-requisitos

- **Python 3.12+**
- **[Poetry](https://python-poetry.org/docs/#installation)** para gerenciamento de dependências

## 🚀 Instalação

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

| Variável                      | Descrição                                | Exemplo                             |
| ----------------------------- | ---------------------------------------- | ----------------------------------- |
| `DATABASE_URL`                | URL de conexão do banco                  | `sqlite+aiosqlite:///./database.db` |
| `SECRET_KEY`                  | Chave usada para assinar os tokens JWT   | `secret_key`                        |
| `ALGORITHM`                   | Algoritmo de assinatura do JWT           | `HS256`                             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do access token (em minutos)    | `30`                                |

> ⚠️ **Importante:** o projeto usa engine assíncrona (`create_async_engine`), então o
> `DATABASE_URL` precisa de um driver async. Para SQLite use
> `sqlite+aiosqlite:///./database.db` (e **não** `sqlite:///./database.db`).
> Em produção, defina uma `SECRET_KEY` forte e única.

## 🗄️ Banco de dados (migrações)

Aplique as migrações antes de subir a aplicação:

```bash
poetry run alembic upgrade head
```

Para criar uma nova migração após alterar os modelos:

```bash
poetry run alembic revision --autogenerate -m "descricao da mudanca"
```

## ▶️ Executando o projeto

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

## 🗂️ Estrutura do projeto

```
simple_todo/
├── app.py            # instancia o FastAPI e registra os routers
├── database.py       # engine e sessão async do SQLAlchemy
├── models.py         # modelos ORM (User, Todo, TodoState)
├── schemas.py        # schemas Pydantic (entrada/saída)
├── security.py       # hash de senha e JWT
├── settings.py       # configurações via .env
└── routes/
    ├── auth.py       # /auth
    ├── users.py      # /users
    └── todo.py       # /todo
tests/                # suíte de testes (pytest)
migrations/           # migrações do Alembic
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
