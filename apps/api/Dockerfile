# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm AS builder

# Configurar uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Instalar uv desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Lockfile obligatorio con --frozen. El código se copia en la imagen final.
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
RUN uv sync --frozen --no-install-project --no-dev --no-install-package radar-api

# Construir aplicación final
FROM python:3.12-slim-bookworm

# Usuario de sistema sin privilegios: el proceso no corre como root
RUN groupadd --system --gid 1001 radar \
    && useradd --system --uid 1001 --gid radar --no-create-home --home-dir /nonexistent --no-log-init radar

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

# Copiar código fuente
COPY apps/api/radar_api /app/radar_api

# Asegurarse de usar Python del entorno virtual
ENV PATH="/app/.venv/bin:$PATH"

# Variables de entorno
ENV RADAR_DATA_DIR="/data"
ENV PORT=8000

USER radar

# Exponer puerto
EXPOSE 8000

# La imagen slim no trae curl; el chequeo usa el Python del entorno virtual.
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ['PORT'] + '/health')"

CMD ["uvicorn", "radar_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
