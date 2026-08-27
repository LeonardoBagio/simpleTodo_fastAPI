# ┌─────────────────────────────────────────────────────────────┐
# │  Simple Todo — FastAPI                                       │
# │  Atalhos para gerenciar os containers Docker (app + banco)  │
# └─────────────────────────────────────────────────────────────┘

# Cores para as mensagens
_green  := '\033[0;32m'
_yellow := '\033[0;33m'
_blue   := '\033[0;34m'
_reset  := '\033[0m'

# Lista as receitas disponíveis (comando padrão)
default:
    @just --list --unsorted

# 🚀  Cria (build) e sobe os containers em segundo plano
create:
    @printf "{{ _blue }}🚀  Buildando as imagens e subindo os containers...{{ _reset }}\n"
    docker compose up -d --build
    @printf "{{ _green }}✅  Pronto! API disponível em http://localhost:8000 (docs em /docs){{ _reset }}\n"

# ▶️  Inicia os containers já criados
start:
    @printf "{{ _blue }}▶️   Iniciando os containers...{{ _reset }}\n"
    docker compose start
    @printf "{{ _green }}✅  Containers em execução em http://localhost:8000{{ _reset }}\n"

# ⏹️  Para os containers sem removê-los
stop:
    @printf "{{ _yellow }}⏹️   Parando os containers...{{ _reset }}\n"
    docker compose stop
    @printf "{{ _green }}✅  Containers parados (dados preservados).{{ _reset }}\n"

# 🧹  Remove os containers e a rede (mantém o volume do banco)
down:
    @printf "{{ _yellow }}🧹  Removendo containers e rede...{{ _reset }}\n"
    docker compose down
    @printf "{{ _green }}✅  Ambiente removido (volume do banco preservado).{{ _reset }}\n"

# 📜  Acompanha os logs da aplicação
logs:
    docker compose logs -f app

# 📊  Mostra o status dos containers
status:
    docker compose ps
