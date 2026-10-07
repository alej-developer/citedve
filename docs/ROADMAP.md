# Hoja de ruta

Todo lo que no está en el esqueleto actual vive aquí. El orden respeta el MVP de 30 días de
[`PRODUCT.md`](PRODUCT.md) y los criterios de «no hacer».

## Hecho (esqueleto v0.1)

- Monorepo, contrato de datos con paridad JSON Schema / Pydantic / TypeScript.
- Scripts de validación y derivación; API de solo lectura; web estática mínima; CI.

## Próximo (semanas 1–2 del MVP)

- `docs/METHODOLOGY.md` v1 y fichas completas del catálogo de fuentes (licencias revisadas).
- Edición piloto en `content/radar/` con las primeras señales reales.
- Comprobador de enlaces vivos y campo `archive_url` en señales críticas.
- Página de edición y archivo de ediciones en `apps/web`.

## Después (semanas 3–4)

- Páginas de metodología, fuentes y descargas; accesibilidad y lectura en móvil.
- Informe de calidad del dato (métricas de `PRODUCT.md` §7).
- Despliegue del sitio estático (Vercel o GitHub Pages) y dominio.

## Más adelante (sujeto a necesidad medida)

- Ingestión asistida (APIs y datos abiertos) con aprobación humana de cada edición.
- Persistencia relacional (SQLAlchemy 2 + Alembic, SQLite → Postgres) si surgen consultas de series.
- Despliegue de la API (Railway/Fly) y series históricas.
- Resumen ejecutivo bilingüe ES/EN.
- Generación automática de tipos TS desde el JSON Schema.
- Metodología documentada para referencias de FX de mercado paralelo.
