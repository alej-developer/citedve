# content/radar

Una edición por semana, en `YYYY-MM-DD.md` (fecha de publicación, lunes). Cada señal de
`data/signals.json` debe referenciar una edición que exista aquí (lo comprueba `scripts/validate_signals.py`).

Estructura obligatoria de cada edición:

1. Titular factual (máx. 2 líneas).
2. Resumen ejecutivo (3–5 viñetas, cada una con cita).
3. Secciones por dominio: FX · Inflación · Energía · Sanciones/OFAC · Fintech/Pagos · E-commerce · Infraestructura digital.
4. Qué cambió frente a la semana anterior.
5. Notas metodológicas y correcciones.
6. Fuentes con fecha de captura.

Cada afirmación se etiqueta como **Hecho**, **Rango entre fuentes** o **Hipótesis**
(ver `docs/DATA_DICTIONARY.md`). Usa `_template.md` como punto de partida; los archivos que
empiezan por `_` se ignoran.
