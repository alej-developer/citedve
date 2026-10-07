# @radar/schema

Contrato de datos de Radar Venezuela.

| Archivo | Rol |
|---------|-----|
| `signals.schema.json` | Fuente de verdad (JSON Schema 2020-12) |
| `src/index.ts` | Espejo TypeScript para `apps/web` |
| `../../apps/api/radar_api/models.py` | Espejo Pydantic v2 para `apps/api` |
| `fixtures/valid.json` | Datos **sintéticos** para pruebas (no son datos reales) |

Un test en `apps/api/tests/test_schema_parity.py` comprueba que JSON Schema y Pydantic aceptan
y rechazan los mismos documentos.

Reglas que el esquema impone:

- `sources` tiene al menos 1 elemento, y cada fuente exige `name`, `url` y `captured_at`.
- `claim_type = range` exige `range`, `unit` y al menos 2 fuentes.
- `claim_type = hypothesis` exige `confidence`, `assumptions` y `falsifiers`.
