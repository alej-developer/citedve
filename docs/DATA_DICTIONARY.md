# Diccionario de datos

Versión de esquema: `0.1.0`. Fuente de verdad: [`packages/schema/signals.schema.json`](../packages/schema/signals.schema.json).

## `data/signals.json`

```json
{ "schema_version": "0.1.0", "signals": [ /* Signal */ ] }
```

### Signal

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `id` | string `^[a-z0-9][a-z0-9-]{2,80}$` | sí | Identificador estable y único |
| `edition` | fecha `YYYY-MM-DD` | sí | Edición semanal; debe existir `content/radar/<edition>.md` |
| `domain` | enum | sí | `fx`, `inflation`, `energy`, `sanctions`, `fintech`, `ecommerce`, `digital_infra` |
| `indicator` | string `dominio.nombre` | sí | Indicador, p. ej. `fx.official_rate` (minúsculas, `_`, separado por `.`) |
| `claim_type` | enum | sí | `fact`, `range`, `hypothesis` |
| `title` | string 3–160 | sí | Titular factual |
| `statement` | string 10–1200 | sí | Enunciado en español neutro |
| `value` | número o `null` | no | Valor puntual (hechos) |
| `unit` | string o `null` | según tipo | Unidad y base (p. ej. `Bs/USD`, `% mensual`) |
| `range` | `{min, max}` | `range` | Mínimo y máximo entre fuentes |
| `observed_at` | fecha | sí | Fecha a la que **se refiere** el dato |
| `sources` | lista de Source | sí | ≥ 1 (≥ 2 si `range`) |
| `confidence` | `low`/`medium`/`high` | `hypothesis` | Confianza declarada |
| `assumptions` | lista de string | `hypothesis` | Premisas explícitas |
| `falsifiers` | lista de string | `hypothesis` | Qué evidencia la refutaría |

### Source

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `name` | string 2–120 | sí | Nombre de la fuente |
| `url` | `http(s)://…` | sí | Enlace exacto al dato |
| `captured_at` | fecha | sí | Día en que se consultó la fuente |
| `published_at` | fecha | no | Fecha de publicación de la fuente |
| `archive_url` | `http(s)://…` | no | Copia archivada (p. ej. Wayback Machine) |

### Reglas por tipo

| `claim_type` | Reglas |
|--------------|--------|
| `fact` | 1 fuente suficiente. |
| `range` | `range` y `unit` obligatorios; ≥ 2 fuentes con URL distinta; `min ≤ max`. |
| `hypothesis` | `confidence`, `assumptions`, `falsifiers` obligatorios. |

### Reglas de integridad (`scripts/validate_signals.py`)

- `id` único.
- `captured_at` de cada fuente ≤ `edition`.
- Existe `content/radar/<edition>.md` para cada edición referenciada.
- Los archivos de `content/radar/` siguen `YYYY-MM-DD.md` (se ignoran `README.md` y los que empiezan por `_`).

## Derivados (no editar a mano)

### `data/latest.json`

`{ schema_version, edition, signals }` con las señales de la edición más reciente (`edition: null` si no hay señales).

### `data/signals.csv`

Una fila por señal, ordenada por `(edition, id)`. Columnas: `id, edition, domain, indicator, claim_type, title,
value, unit, range_min, range_max, observed_at, confidence, source_names, source_urls, source_captured_at`.
Las listas de fuentes se unen con ` | ` y mantienen el mismo orden entre columnas.

Se regeneran con `uv run python scripts/build_data.py`; CI falla si están desactualizados.
