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

## Observaciones FX (`0.1.0`)

Contrato separado. Fuente de verdad: [`packages/schema/fx_observations.schema.json`](../packages/schema/fx_observations.schema.json). No modifica `signals.schema.json`. Los espejos son `packages/schema/src/fx.ts` y `apps/api/radar_api/models_fx.py`.

Documento: `schema_version`, `editions[]`, `observations[]`. Una edición vacía (`editions: []`, `observations: []`) es válida. Los ficheros de `packages/schema/fixtures/` son sintéticos y no se publican como datos reales.

### Edition

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `id` | `^\d{4}-W\d{2}$` | sí | Semana ISO |
| `cutoff_date` | fecha | sí | Fecha de corte. El corte semanal es el viernes |
| `status` | enum | sí | `draft`, `published`, `retracted` |
| `p2p_status` | enum | sí | `publicado` o `sin_dato` |
| `retraction_reason` | string | si `retracted` | Motivo. Obligatorio y no vacío cuando la edición está retirada |
| `notes` | string | no | Texto factual. Sin datos personales |

### Observation

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `id` | `fx-{edition}-{indicator}-{institution}-{side}` | sí | Identificador estable |
| `edition` | semana ISO | sí | Debe existir en `editions` (lo comprueba el validador) |
| `indicator` | enum | sí | `tasa_oficial_bcv`, `tasa_informativa_banco`, `p2p_referencia`. Ampliar exige un ADR |
| `institution.id` | slug | sí | `^[a-z0-9-]+$` |
| `institution.name` | string | sí | Nombre tal como lo escribe la fuente |
| `institution.kind` | enum | sí | `banco_central`, `banco`, `agregado_fuente`, `mercado_p2p` |
| `side` | enum | sí | `compra`, `venta`, `referencia` |
| `value` | número > 0 | sí | Finito |
| `value_as_published` | string | sí | Texto literal de la fuente, para auditar la transcripción |
| `unit` | enum | sí | `VES/USD` (BCV y bancos) o `VES/USDT` (P2P). USDT no es USD |
| `as_of_date` | fecha | sí | Fecha del dato |
| `date_basis` | enum | sí | `fecha_valor`, `fecha_operacion`, `fecha_indicador`, `captura_archivada` |
| `operation_date` | fecha | si tasa oficial | Fecha de operación del libro SMC. Es la fecha que manda para el BCV |
| `status` | enum | sí | `published` o `retracted` |
| `retraction_reason` | string | si `retracted` | Motivo. Se oculta el valor retirado en la página |
| `source.name` | string | sí | Nombre de la fuente |
| `source.publisher_id` | slug | sí | Editor (`bcv`, `usdt-com-ve`) |
| `source.upstream_id` | slug | no | Mercado de origen en P2P (`binance-p2p`, `bybit-p2p`). La independencia se mide por este campo |
| `source.url` | `https://…` | sí | URL exacta del dato, no la portada |
| `source.locator` | string | si la URL acaba en `.xls` | Hoja, filtro o fila |
| `source.accessed_at` | datetime con zona | sí | Momento de consulta. No anterior a `as_of_date` |
| `source.archive_url` | `https://…` | si P2P | URL archivada con fecha. La página viva no basta |
| `source.sha256` | 64 hex | si la URL acaba en `.xls` | El libro SMC se sobrescribe; el hash fija el archivo |
| `source.license` | string | sí | Términos con los que se cita |
| `notes` | string | no | Por ejemplo, que la fuente publica compra mayor que venta |

No hay campo para quien captura.

### Reglas que el esquema ya impone

- `https` solamente.
- `value` estrictamente mayor que 0.
- Edición u observación `retracted`: `retraction_reason` no vacío.
- `tasa_oficial_bcv`: `operation_date`.
- `p2p_referencia`: `source.archive_url`.
- URL que termina en `.xls`: `sha256` y `locator`.

Las reglas entre filas las aplica [`scripts/validate_fx.py`](../scripts/validate_fx.py), no este esquema: una tasa oficial por lado, al menos 3 bancos, P2P con al menos 2 `upstream_id` distintos o `sin_dato`, corte en viernes, fecha de operación, dominios permitidos y vetos. La definición de independencia y el umbral de «desactualizado» (más de 8 días) están en el ADR-0001 y en `docs/SOURCES.md`. `scripts/build_fx.py` regenera `data/fx/latest.json` y `data/fx/observations.csv`.
