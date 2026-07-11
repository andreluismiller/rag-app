FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o uv copiando o binario oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/workspace/.venv

WORKDIR /workspace

# Copia os arquivos de definicao de dependencias primeiro (cache de camadas).
# "uv.lock*" (com asterisco) torna o lockfile opcional: se nao existir no
# contexto de build, o COPY nao falha e o uv sync abaixo o gera na hora.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project --no-dev

# Copia o restante do codigo
COPY . .
RUN uv sync --no-dev

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/Home.py", \
     "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
