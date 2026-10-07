# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm AS builder

# Configurar uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Instalar uv desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar configuración de dependencias
COPY pyproject.toml .
RUN uv sync --frozen --no-install-project --no-dev

# Construir aplicación final
FROM python:3.12-slim-bookworm

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

# Copiar código fuente
COPY apps/api/radar_api /app/radar_api

# Asegurarse de usar Python del entorno virtual
ENV PATH="/app/.venv/bin:$PATH"

# Variables de entorno
ENV RADAR_DATA_DIR="/data"
ENV PORT=8000

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

CMD ["uvicorn", "radar_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
