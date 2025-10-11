# =========================
# 1) Imagem base para build
# =========================
FROM python:3.12-slim AS builder

# envs
ENV POETRY_VERSION=2.2.0 \
    PYTHONUNBUFFERED=1
#    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependências do sistema necessárias para compilar libs (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Instala Poetry no container
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Export requirements.txt
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN poetry run poe export_requirements_prod

RUN grep -E '^newrelic([=<>]|$)' requirements.txt >/dev/null \
  || (echo 'ERRO: newrelic não foi exportado para requirements.txt' >&2; exit 1)

COPY ./src/ ./src/

# =========================
# 2) Runtime stage
# =========================
FROM python:3.12-slim AS runtime

# envs
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    GUNICORN_WORKERS=4

RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m fastapiuser
USER fastapiuser

WORKDIR /app

COPY --from=builder /app /app
COPY --chown=fastapiuser:fastapiuser newrelic.ini /app/newrelic.ini

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/api/v1/health || exit 1

# Instala gunicorn + uvicorn[standard] no runtime
USER root
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "gunicorn==22.0.0" "uvicorn[standard]==0.37.0"

USER fastapiuser

CMD ["/bin/sh", "-c", "\
  NEW_RELIC_CONFIG_FILE=/app/newrelic.ini \
  exec newrelic-admin run-program \
  gunicorn -k uvicorn.workers.UvicornWorker src.api.Main:app \
  -w \"$GUNICORN_WORKERS\" -b 0.0.0.0:8000 \
  --access-logfile - --error-logfile - \
  --keep-alive 5 --timeout 30 \
"]