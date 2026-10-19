# ADR-0001: Panel de tasas por banco y brecha BCV–P2P antes de levantar el «no hacer» n.º 10

- **Estado:** Aceptado
- **Fecha:** 2026-10-19
- **Ámbito:** `docs/PRODUCT.md` §8 («no hacer» n.º 10 y criterio de salida), dominio FX
- **Numeración:** es el ADR-0001 porque `docs/decisions/` todavía no existía en `main` cuando se redactó (comprobado el 2026-10-19 sobre el commit `275581b`). Este ADR creó la carpeta. El documento de planes usaba otros números provisionales (ADR-0003 para este panel); quedan sustituidos.
- **Ubicación:** `docs/decisions/ADR-0001-panel-tasas.md`.

## Contexto

1. **La regla.** PRODUCT §8, «no hacer» n.º 10: «No añadir dominios o indicadores nuevos hasta cumplir las métricas de calidad de los existentes durante 4 semanas». El criterio de salida de §8 exige, para reabrir una restricción: (a) una necesidad de usuario documentada, (b) un plan para preservar la trazabilidad y (c) un ADR en `docs/decisions/`.
2. **Las 4 semanas no han empezado a contar.** La regla no caduca en una fecha fija: se levanta tras 4 semanas *cumpliendo* las métricas de §7. Hoy no se cumplen. Tras el PR #4 (fusionado el 2026-10-19), `data/signals.json` tiene 4 señales con fecha del dato hasta el 2026-10-07, y en FX solo hay una publicada (BCV oficial, 873,867 Bs/USD, con el libro SMC del BCV como fuente). La única referencia paralela (991,99) quedó `retracted` porque no había una página con fecha que la respaldara. En consecuencia, la métrica «multiplicidad de fuentes, FX: 100 %» y la obligación del MVP de mostrar el FX como «tasa oficial BCV vs. al menos 2 referencias alternativas» (PRODUCT §6) **no se cumplen**.
3. **El panel ataca justo ese incumplimiento.** El plan (`planes-ideas-radar.md`, sección «Idea 2. Panel de tasas por banco y brecha BCV vs P2P») modela el FX como **observaciones** citadas por institución y lado (compra/venta), con un rango P2P de ≥ 2 fuentes por fecha. Es la entidad «Observación» que PRODUCT §5 ya define, y todavía no está implementada.
4. **Necesidad de usuario.** Es la persona «operador de fintech/pagos» y el segmento «diáspora y operadores» de PRODUCT §2, en el job to be done n.º 3 («ver cuánto discrepan las fuentes antes de decidir»). Las tasas por banco y la brecha están dispersas entre el BCV y varios agregadores (plan, idea 2). Ojo: esta necesidad está **argumentada en el plan, no medida** con usuarios. Lo cuento como límite de este ADR.
5. **Estado del repo.** El PR #4 dejó listos los requisitos previos: fuentes con URL exacta, `FxGapMeter` calculado con las dos tasas y con tests, y CONTRIBUTING alineado con el esquema `0.1.0`. El PR #5 (borrador, solo documentación) dice que la API no implementa los filtros `domain`, `claim_type` ni `edition`. La demo pública no tiene despliegue (PR #4).
6. **Prioridad.** El dueño decidió que el panel va antes que la guía para personas regularizadas.

## Decisión

Se reabre el «no hacer» n.º 10 **solo** para el panel de tasas, con el alcance y los guardarraíles de abajo. Cualquier otro dominio o indicador sigue bloqueado y necesita su propio ADR.

**Alcance del MVP:**
- Contrato nuevo y separado: `packages/schema/fx_observations.schema.json`, su espejo TS, su espejo Pydantic y su test de paridad. No se modifica `signals.schema.json`.
- `data/fx/observations.json`, mantenido a mano por PR, como fuente de verdad; derivados generados por script con `--check` en CI.
- Cálculo puro en `apps/api/radar_api/fx.py`: brecha, dispersión entre bancos, mediana y rango P2P, con tests.
- Página estática `/fx` con tabla por banco, rango P2P, fecha de corte y fuentes en cada fila.
- Fuera del MVP: endpoints de la API, serie histórica, gráficos, calculadora de margen y resumen en inglés. Cada uno entra después en un PR aparte, y la calculadora necesita una revisión propia (ver guardarraíles).

## Alternativas consideradas

| Alternativa | A favor | En contra | Resultado |
|---|---|---|---|
| **A. Esperar a cumplir 4 semanas de métricas** | Es lo que dice la regla al pie de la letra; sin riesgo de alcance | Con FX en una sola fuente publicada, la métrica de multiplicidad no se puede cumplir sin crear antes un modelo de observaciones con ≥ 2 referencias, que es justo lo que propone el panel. La espera no tiene fecha de fin | Descartada |
| **B. Cargar más referencias como señales sueltas en `signals.json`** | No cambia el contrato | El esquema no tiene `claim_type` ni rango, ni compra/venta por institución. Forzarlo mezcla señales cualitativas con series y empeora la trazabilidad | Descartada |
| **C. Panel completo de una vez (API, serie, calculadora)** | Más vistoso | Más superficie de error. La calculadora roza el «no hacer» n.º 7 (señales de trading) | Descartada |
| **D. Panel acotado con ADR (esta decisión)** | Cumple el criterio de salida de §8 y ataca el incumplimiento actual de FX | Añade un contrato nuevo que mantener | **Elegida** |

## Decisiones del dueño (2026-10-19)

Cierran las tres preguntas abiertas del plan de implementación. La misma redacción está en `docs/SOURCES.md`.

1. **Independencia P2P.** Las medianas de Binance y de Bybit publicadas por usdt.com.ve cuentan como 2 fuentes para la regla «≥ 2 fuentes». La independencia se mide por `upstream_id` distinto (`binance-p2p` y `bybit-p2p`), aunque el `publisher_id` sea el mismo. Limitación de editor único: hay un solo editor. El panel lo dice de forma explícita cuando solo hay un editor. No son dos editores independientes.
2. **Corte y frescura.** El corte semanal es el viernes. La fecha que manda para la tasa oficial del BCV es la fecha de operación, no la fecha valor. Se muestra el aviso «desactualizado» cuando el corte tiene más de 8 días (`hoy − cutoff_date > 8`).
3. **Brecha.** Se muestra la brecha frente al mínimo, al máximo y a la mediana P2P. Cada una va etiquetada.

## Consecuencias

- **Positivas:** el FX pasa a mostrarse como rango entre fuentes («no hacer» n.º 3), PRODUCT §5 implementa por fin la «Observación» y hay una métrica de multiplicidad que se puede medir.
- **Negativas:** un segundo contrato, con paridad triple propia que mantener; unos 30–45 min por semana de captura manual citada; y el riesgo de que las tasas por banco se lean como cotización en vivo, cuando son una foto semanal.
- **Sobre la regla n.º 10:** el reloj de 4 semanas para cualquier *otro* dominio nuevo empieza a contar cuando FX cumpla sus métricas, no antes. La guía para personas regularizadas sigue necesitando su propio ADR.

## Guardarraíles

1. **Qué cuenta como indicador.** Una magnitud con valor, unidad y fecha del dato que se publica de forma recurrente para su comparación en el tiempo. En este panel lo son: la tasa por institución y lado, la mediana y el rango P2P por fecha, la brecha BCV–P2P y la dispersión entre bancos. **No son indicadores nuevos:** las vistas de presentación (tabla, ordenación) ni los cálculos auxiliares que no se publican. Cualquier magnitud fuera de esta lista (comisiones de casas de cambio, remesas, inflación por banco…) necesita otro ADR.
2. **Fuentes según PRODUCT §8 n.º 1, 3 y 5.**
   - Cada observación lleva fuente, `accessed_at`, URL exacta del dato (no la portada) y fecha del dato. Sin estos campos, el validador la rechaza.
   - El P2P solo se publica como rango de ≥ 2 fuentes independientes por fecha. Qué cuenta como independiente lo fija la decisión del dueño de este ADR (`upstream_id` distinto). Con una sola fuente, «sin dato disponible», nunca imputado.
   - Precedente del PR #4: una cifra sin página con fecha no se carga, o se marca `retracted`.
   - Ingreso manual citado. Sin scraping que viole ToS o robots.txt, y nada de la API interna de Binance P2P (`/bapi/` está en Disallow).
3. **Sin ranking ni recomendaciones.**
   - Sin «mejor tasa», ni orden por conveniencia, ni resaltar a ningún banco, casa de cambio o plataforma. Orden por defecto: alfabético o el de la propia fuente.
   - Sin enlaces de afiliado ni publicidad.
   - Sin llamadas a la acción («compra», «vende», «ahora»): «no hacer» n.º 7.
   - Fuera del MVP no se listan casas de cambio ni operadores de remesas.
4. **Presentación honesta.** Fecha de corte visible y aviso de «foto semanal, no cotización en vivo; información, no asesoramiento». Se publican unidades y lado (compra/venta), y las discrepancias se muestran, no se ocultan.
5. **Privacidad.** Sin datos personales en el repo ni capturas con datos de terceros («no hacer» n.º 14).

## Métricas de éxito

Se revisan al cerrar cada edición semanal.

| Métrica (PRODUCT §7) | Objetivo |
|---|---|
| Cobertura de citación de las observaciones FX | 100 %, bloqueante en CI |
| Multiplicidad FX (fechas con P2P de ≥ 2 fuentes) | 100 % de las fechas publicadas |
| Enlaces vivos de las fuentes FX | ≥ 98 % |
| Frescura | Cada fecha publicada dentro del umbral declarado; si no, «desactualizado» |
| Puntualidad | Observaciones de la semana cargadas en ≥ 90 % de las ediciones |
| CI | Verde con validación FX, paridad y tests de cálculo |

Criterio de «hecho» del MVP: el del plan, idea 2 (≥ 3 semanas de datos, ≥ 3 bancos por fecha, P2P con ≥ 2 fuentes por fecha, `/fx` con fecha de corte y fuentes por fila).

## Criterios de reversión

Se congela el panel (se retira `/fx` de la navegación y los datos se quedan en Git) y se vuelve a la regla n.º 10 sin excepciones si ocurre cualquiera de estas cosas:
- Dos ediciones seguidas con P2P de una sola fuente o con observaciones sin URL exacta.
- Una corrección de una cifra FX publicada sin respuesta en < 72 h (PRODUCT §7).
- Cualquier elemento que funcione como ranking o recomendación, o una queja razonada en ese sentido que no se resuelva en el siguiente PR.
- Que no se sostenga la captura manual semanal durante 3 semanas (fatiga del mantenedor, PRODUCT §9).
- Una restricción legal o de ToS de una fuente que impida citarla, sin alternativa equivalente.

La reversión se registra en un ADR nuevo que sustituye a este.

## Referencias

- `docs/PRODUCT.md` §2, §5, §6, §7, §8 y §9.
- PR #4 (fusionado): fuentes exactas, retirada de la tasa paralela, `FxGapMeter` con tests y CONTRIBUTING alineado.
- PR #5 (borrador): documentación real de la API.
- `/workspace/citedve-planes/planes-ideas-radar.md`, sección «Idea 2. Panel de tasas por banco y brecha BCV vs P2P».
