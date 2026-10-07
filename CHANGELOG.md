# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere al [Versionamiento Semántico](https://semver.org/lang/es/).

## [0.1.0] - 2026-10-07

### Added
- **Arquitectura Base (Git-as-Database)**: Diseño de monorepo gestionando contratos y esquemas JSON compartidos (`@radar/schema`).
- **Data Pipeline Local**: Scripts en Python (`validate_signals.py` y `build_data.py`) para validar el esquema e integrarlo en artefactos estáticos (CSV, `latest.json`).
- **Automatización**: Script `make radar` (via Python `new_radar_week.py`) que aplica un *Human-in-the-loop* para generar reportes semanales limpios.
- **API (Lectura)**: Backend FastAPI que expone los datos bajo un modelo espejo en Pydantic v2 (listo para extensión futura).
- **Web App (SSG)**: Frontend en Next.js (App Router) y Tailwind CSS v4, compilado al 100% como exportación estática con un diseño editorial, tipográfico y minimalista.
- **Componentes React Visuales**: `FxGapMeter`, `SignalRow`, y `ConfidencePill`.
- **Plantillas GitHub**: Formularios de Issue y PR diseñados para rechazar información sin fuente primaria (`.github/ISSUE_TEMPLATE/*`).
- **Release Initial (Radar)**: Primera publicación oficial con datos verídicos al corte actual.

### Changed
- Tipos de TypeScript migrados del diseño conceptual viejo al esquema final de `Signal` en `packages/schema`.

### Fixed
- Manejo de caracteres UTF-8 en el CLI script de Python (`new_radar_week.py`).
