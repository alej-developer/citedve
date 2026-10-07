# Diccionario de datos

Versión de esquema: `0.1.0`. Fuente de verdad: [`packages/schema/signals.schema.json`](../packages/schema/signals.schema.json).

## `data/signals.json`

```json
{ "schema_version": "0.1.0", "signals": [ /* Signal */ ] }
```

### Signal

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `id` | string `^[a-z0-9][a-z0-9-]{2,80}$` | sí | Identificador estable (slug) |
| `title` | string 3–160 | sí | Titular de la señal |
| `category` | enum | sí | `fx`, `inflation`, `energy`, `sanctions`, `fintech`, `ecommerce`, `digital_infra`, `politics_risk`, `other` |
| `summary` | string ≤280 | sí | Resumen factual |
| `value_numeric` | número o `null` | no | Valor numérico, si aplica |
| `value_text` | string o `null` | no | Valor de texto, si aplica |
| `unit` | string o `null` | no | Unidad (p. ej. `Bs/USD`) |
| `as_of_date` | fecha `YYYY-MM-DD` | sí | Fecha de referencia del dato |
| `captured_at` | datetime (ISO) | sí | Fecha y hora (timezone-aware) de captura |
| `direction` | enum | sí | `up`, `down`, `flat`, `mixed`, `n/a` |
| `confidence` | enum | sí | `high` (fuente primaria oficial), `medium` (prensa seria), `low` (estimado) |
| `sources` | lista de Source | si `published` | Fuentes (mínimo 1 si publicado) |
| `tags` | lista de string | sí | Etiquetas relevantes |
| `region` | string | sí | Por defecto `"VE"` |
| `notes` | string o `null` | no | Notas opcionales (ej. para rangos entre fuentes) |
| `status` | enum | sí | `published`, `draft`, `retracted` |

### Source

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `name` | string 2–120 | sí | Nombre de la fuente |
| `url` | `http(s)://…` | sí | Enlace exacto al dato |
| `accessed_at` | fecha `YYYY-MM-DD`| sí | Día en que se consultó la fuente |

### Reglas de integridad (`scripts/validate_signals.py`)

- `id` único.
- Toda señal `published` exige ≥1 source con URL.
- Prohibido inventar cifras. Si falta dato, no se crea la señal (o queda como `draft`).

## Derivados (no editar a mano)

### `data/latest.json`

Contiene las 50 señales más recientes ordenadas por fecha de captura.

### `data/signals.csv`

Una fila por señal. Columnas alineadas con las propiedades del objeto `Signal`. Se regeneran con `uv run python scripts/build_data.py`; CI falla si están desactualizados.
