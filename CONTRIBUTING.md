# Cómo contribuir

Gracias por querer mejorar CitedVE. Antes de empezar, lee [`docs/PRODUCT.md`](docs/PRODUCT.md)
(principios y criterios de «no hacer») y el [Código de conducta](CODE_OF_CONDUCT.md).

## Entorno local

Requisitos: [uv](https://docs.astral.sh/uv/) y Node.js 22 o superior.

```bash
uv sync                 # entorno Python 3.12 (api + scripts + herramientas)
npm install             # dependencias web (workspaces)
```

## Contribuir una señal

1. Verifica que la fuente es **pública** y que puedes citarla.
2. Añade el objeto a `data/signals.json` siguiendo `docs/DATA_DICTIONARY.md`. Reglas:
   - `sources` con `name`, `url` y `captured_at` (fecha en que **tú** consultaste la fuente).
   - `claim_type = fact`: una fuente. `range`: al menos 2 fuentes distintas, con `range.min/max` y `unit`.
     `hypothesis`: `confidence`, `assumptions` y `falsifiers`.
   - Sin cifras «de memoria»; sin opinión presentada como hecho.
3. Crea o actualiza la edición `content/radar/YYYY-MM-DD.md` (parte de `_template.md`).
4. Regenera y valida:

   ```bash
   uv run python scripts/build_data.py
   uv run python scripts/validate_signals.py
   ```
5. Abre un PR. Describe la fuente y cómo verificar la cifra.

Corrección de un dato: abre un issue con la señal afectada, la fuente correcta y el enlace.

## Verificación antes del PR

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy apps/api scripts
uv run pytest
npm run web:lint && npm run web:typecheck && npm run web:build
```

## Cambios de contrato de datos

Si tocas el esquema, actualiza los tres lugares: `packages/schema/signals.schema.json`,
`packages/schema/src/index.ts` y `apps/api/radar_api/models.py`. El test de paridad debe seguir en verde.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/): `feat:`, `fix:`, `docs:`,
`chore:`, `ci:`, `test:`, `refactor:`, `data:` (altas o correcciones de señales).

## Qué no aceptamos

Ver la sección 8 de [`docs/PRODUCT.md`](docs/PRODUCT.md): cifras sin fuente, scraping que viole términos
de servicio, recomendaciones de inversión, contenido político partidista o material con propiedad
intelectual ajena.

## Licencia de las contribuciones

Al contribuir aceptas que tu aportación se publique bajo Apache-2.0 (código) y CC BY 4.0 (datos y
contenido editorial propios).
