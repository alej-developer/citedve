# Sistema Visual y Diseño (Radar Venezuela)

## Filosofía
Radar Venezuela no es una startup B2B SaaS promocionando su "AI". Es un **observatorio institucional y editorial**. Los usuarios vienen a consumir hechos densos con alta confianza y trazabilidad.

**Principios:**
- **Seriedad por encima del "Wow":** Nada de blobs, glassmorphism o animaciones complejas de 3D. 
- **Jerarquía de publicación:** Usamos tipografías sólidas y alto contraste. Layout que facilita la lectura (max-width conservador, espacios en blanco).
- **El dato como protagonista:** Tabular figures para los números, colores de acento reservados estrictamente para la semántica del dato (verde para aumento, rojo para contracción/alarma, slate para plano).
- **Microinteracciones:** Mínimas. Preferimos claridad antes que motion. Las interacciones se limitan a `opacity` sutil y un pequeño `transform` en enlaces clave (200ms).

## Fichas Tipográficas
1. **Titulares (Newsreader):** Elegida por su legado editorial y excelente legibilidad en pantallas. Transmite rigor periodístico y seriedad institucional.
2. **UI & Datos (IBM Plex Sans):** Grotesca, técnica y con excelentes números tabulares (`font-variant-numeric: tabular-nums`). Ideal para leer métricas, tasas y metadatos sin ambigüedad (los unos, los ceros y las eles no se confunden).

## Paleta de Colores
- **Fondo (Paper):** Off-white cálido (`#F9F9F8`) en modo claro. En modo oscuro, un casi-negro absoluto (`#111111`).
- **Texto (Ink):** Near-black (`#111111`) en claro para AA contrast; off-white (`#EDEDED`) en oscuro. No usamos #000 ni #FFF absolutos para reducir fatiga visual.
- **Acentos semánticos:**
  - `up`: Verde petróleo (`#0F5B46`). Representa alzas (no necesariamente positivas moralmente, ej: inflación) pero mantiene legibilidad sobre el papel.
  - `down`: Rojo constricción (`#991b1b`). Representa bajas o alarmas.
  - `flat`: Slate (`#4b5563`). Sin cambios o neutro.

## Componentes Clave
- **SignalRow:** Reemplaza a las "cards" tradicionales (border-radius y box-shadow genérico). En diseño editorial, las filas separadas por *rules* (líneas de 1px) son más limpias y escaneables.
- **FxGapMeter:** Visualización SVG minimalista en línea para mostrar la brecha cambiaria. Aporta contexto visual sin necesitar librerías de gráficas pesadas.
- **ConfidencePill:** Píldoras austeras. En lugar de fondos con colores arcoíris, varían por opacidad, color del texto y tipo de borde (sólido vs dashed) para indicar visualmente la robustez de la fuente.

## Modo Oscuro
El dark mode se aplica de manera automática (`@media prefers-color-scheme`). Evita la inversión bruta; ajusta el contraste semántico para que los acentos mantengan legibilidad AA sin ser fosforescentes distractores.
