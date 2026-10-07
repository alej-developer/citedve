# radar-api

API de solo lectura sobre `data/signals.json`.

```bash
uv sync
uv run uvicorn radar_api.main:app --reload --app-dir apps/api
# http://127.0.0.1:8000/docs
```

Variable opcional: `RADAR_DATA_DIR` (por defecto, `data/` en la raíz del repo).

| Endpoint | Descripción |
|----------|-------------|
| `GET /health` | Estado |
| `GET /v1/signals` | Lista con filtros `domain`, `claim_type`, `edition`, `limit` |
| `GET /v1/signals/latest` | Última edición |
| `GET /v1/signals/{id}` | Una señal |
