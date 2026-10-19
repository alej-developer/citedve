# radar-api

API de solo lectura. Carga `signals.json` y no escribe datos.

## Arranque

Desde la raíz del repo:

```bash
uv sync
uv run uvicorn radar_api.main:app --reload --app-dir apps/api
# http://127.0.0.1:8000/docs
```

`/docs`, `/redoc` y `/openapi.json` los genera FastAPI. No son rutas de producto.

## Datos y entorno

El proceso lee `{directorio}/signals.json`. No lee `latest.json`.

| Variable | Efecto | Valor por defecto |
|----------|--------|-------------------|
| `RADAR_DATA_DIR` | Directorio de `signals.json` | `../../data`, relativo al directorio de trabajo del proceso |
| `RADAR_CORS_ORIGINS` | Orígenes CORS permitidos | `["*"]` |

CORS admite `GET` y `OPTIONS`.

## Endpoints

### `GET /health`

Respuesta: `{"status": "ok", "version": "0.1.0"}`. `version` es la versión del paquete.

### `GET /v1/signals`

Lista paginada. Cuerpo: `{"items": [Signal], "next_cursor": string | null}`.

Orden: `captured_at` descendente.

| Parámetro | Tipo | Efecto |
|-----------|------|--------|
| `category` | enum | Coincide con `category`. Valores: `fx`, `inflation`, `energy`, `sanctions`, `fintech`, `ecommerce`, `digital_infra`, `politics_risk`, `other`. Otro valor responde 422. |
| `from` | fecha `YYYY-MM-DD` | Incluye señales con `as_of_date` mayor o igual. |
| `to` | fecha `YYYY-MM-DD` | Incluye señales con `as_of_date` menor o igual. |
| `tag` | string | La señal contiene ese tag. |
| `limit` | entero | Tamaño de página. Por defecto 50. Mínimo 1, máximo 100. Fuera de rango responde 422. |
| `cursor` | string | Id ya visto. La página empieza en la señal siguiente de la lista filtrada. Si el id no está en esa lista, `items` queda vacío. |

`next_cursor` es el id del último elemento de la página cuando aún quedan señales. Si no quedan, es `null`.

### `GET /v1/signals/{signal_id}`

Una señal. Si el id no existe, responde 404 con detalle `Señal no encontrada`.

### `GET /v1/radar/latest`

Hasta 50 señales, con el mismo orden que la lista, y `schema_version` `0.1.0`. Sale de `signals.json`.

### `GET /v1/meta/categories`

Lista de los valores de `category`.

### `GET /v1/meta/sources`

Nombres de fuente distintos, ordenados, tomados de las señales cargadas.

## No implementado todavía

La API no acepta estos filtros ni esta ruta:

- `claim_type`
- `domain`
- `edition`
- `GET /v1/signals/latest` (la ruta que existe es `GET /v1/radar/latest`)
