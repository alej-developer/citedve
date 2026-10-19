# @radar/schema

Contrato de datos de CitedVE.

| Archivo | Rol |
|---------|-----|
| `signals.schema.json` | Fuente de verdad (JSON Schema 2020-12) |
| `src/index.ts` | Espejo TypeScript para `apps/web` |
| `../../apps/api/radar_api/models.py` | Espejo Pydantic v2 para `apps/api` |
| `fixtures/valid.json` | Datos **sintéticos** para pruebas (no son datos reales) |

Un test en `apps/api/tests/test_schema_parity.py` comprueba que JSON Schema y Pydantic aceptan
y rechazan los mismos documentos.

Reglas que el esquema `0.1.0` impone:

- Cada fuente exige `name`, `url` y `accessed_at` (fecha `YYYY-MM-DD`).
- Una señal `published` exige al menos una fuente. `captured_at` es un campo de la señal, no de la fuente.
- No hay `claim_type`, `range`, `assumptions` ni `falsifiers`. Esos conceptos no forman parte de este contrato.
