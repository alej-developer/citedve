# Radar Venezuela — Documento de producto

> Estado: borrador v0.1 · Alcance: visión, audiencia, anti-objetivos, MVP a 30 días, métricas de calidad del dato y criterios de «no hacer». No incluye diseño técnico detallado ni código.

---

## 1. Visión

**Radar Venezuela es un observatorio abierto que publica cada semana un resumen citado de las señales económicas y digitales del país**: tipo de cambio, inflación, energía, sanciones/OFAC, fintech y pagos, comercio electrónico e infraestructura digital.

Una frase: *«Lo que cambió esta semana en Venezuela, con fuente, fecha y enlace, y sin opinión disfrazada de dato».*

### Qué problema resuelve
- La información sobre Venezuela está dispersa (BCV, paralelo, ONG, prensa, OFAC, reguladores, operadores) y **las fuentes se contradicen**. Cualquier cifra aislada es engañosa.
- Los análisis existentes suelen ser de pago, de opinión, o sin trazabilidad.
- Quien decide (invertir, operar, enviar remesas, lanzar un producto) necesita saber **qué es hecho, qué es rango entre fuentes y qué es hipótesis**.

### Propuesta de valor
1. **Trazabilidad total**: toda cifra con fuente, fecha de captura y enlace.
2. **Honestidad epistémica**: separación explícita entre *hecho*, *rango entre fuentes* e *hipótesis*.
3. **Datos reutilizables**: cada edición produce Markdown legible y JSON/CSV versionados en Git.
4. **Reproducibilidad**: el historial de cambios es público (Git es el registro de auditoría).

### Principios de producto
| # | Principio | Implicación concreta |
|---|-----------|----------------------|
| 1 | Cada cifra lleva fuente, fecha de captura y enlace | Una cifra sin esos tres campos no se publica; el esquema lo rechaza. |
| 2 | Hecho ≠ rango ≠ hipótesis | Tres tipos de afirmación con etiqueta visual y semántica distintas. |
| 3 | Señal sobre ruido | Pocas señales por edición, con criterio editorial documentado. |
| 4 | Español neutro profesional | Tú o impersonal; nunca «vosotros». Sin jerga innecesaria ni tono militante. |
| 5 | Abierto y auditable | Código, datos y metodología públicos. Correcciones visibles. |
| 6 | Diseño institucional sobrio | Referencia: observatorio / publicación de datos, no startup SaaS. |

### Decisiones de licencia (preliminar)
- **Código: Apache-2.0.** Incluye concesión explícita de patentes y cláusula de atribución clara; es más adecuada para un proyecto que aspira a ser adoptado por terceros (instituciones, empresas).
- **Datos y contenido editorial (`data/`, `content/`)**: se propone **CC BY 4.0** para permitir reutilización con atribución. *Nota*: los datos de terceros conservan su licencia original; se documentará fuente por fuente qué se puede redistribuir.
- Se formalizará en `LICENSE`, `NOTICE` y `README` en un paso posterior.

---

## 2. Audiencia

### Primaria
| Segmento | Qué necesita | Qué hace con Radar |
|----------|--------------|---------------------|
| **Inversores, fundadores y analistas** que miran el país | Contexto fiable, comparable en el tiempo, citable en memos | Lee la edición semanal, descarga series, cita con enlace permanente. |
| **Diáspora y operadores** (remesas, pagos, comercio, logística) | Resumen breve y verificable para decisiones prácticas | Consulta el resumen, compara FX entre fuentes, revisa cambios regulatorios. |

### Secundaria
- **Periodistas e investigadores**: usan los datos abiertos y la metodología.
- **Desarrolladores/contribuidores open-source**: añaden fuentes y validaciones.
- **Reclutadores y pares técnicos** (portafolio): evalúan la calidad de producto de datos y la ejecución full stack.

### Jobs to be done
1. «Quiero saber en 3 minutos qué cambió esta semana y con qué respaldo».
2. «Necesito una cifra que pueda citar en un documento sin que me la cuestionen».
3. «Quiero ver cuánto discrepan las fuentes antes de decidir».
4. «Quiero descargar la serie y reutilizarla».

### Personas de referencia (para decisiones de diseño)
- **Analista de fondo/VC** (inglés y español): escanea, copia cifras, exige enlace.
- **Operador de fintech/pagos**: busca cambios de FX, regulación y rieles de pago.
- **Miembro de la diáspora**: quiere contexto sin ruido político; lectura móvil.

---

## 3. Anti-objetivos

Radar Venezuela **no es**:

- **Un blog de opinión.** Las hipótesis existen, pero están etiquetadas, justificadas y separadas de los hechos.
- **Un chatbot ni un asistente conversacional.** Sin interfaz de chat en el MVP ni en el corto plazo.
- **Un dashboard genérico.** Nada de paneles con 30 widgets, gradientes púrpura o métricas de vanidad. Cada visualización responde a una pregunta concreta.
- **Un medio de noticias de última hora.** Cadencia semanal; no compite en inmediatez.
- **Una herramienta de recomendación de inversión o asesoría legal/financiera.** Es información, no consejo.
- **Una plataforma política.** No toma posición partidista; describe señales.
- **Un agregador automático sin supervisión.** La automatización captura y valida; un humano aprueba cada edición.
- **Un producto con datos privados o personales.** Solo fuentes públicas y citables.

Fuera de alcance por política: cualquier contenido o propiedad intelectual de empleos previos del autor queda excluido por completo.

---

## 4. Estructura editorial de cada edición

Cada edición semanal (`content/radar/AAAA-Wnn.md`) sigue una estructura fija:

1. **Titular de la semana** (máx. 2 líneas, factual).
2. **Resumen ejecutivo** (3–5 viñetas, cada una con cita).
3. **Secciones por dominio**: FX · Inflación · Energía · Sanciones/OFAC · Fintech/Pagos · E-commerce · Infraestructura digital.
4. **Cada afirmación se etiqueta** con uno de tres tipos:

| Tipo | Definición | Ejemplo | Requisitos |
|------|------------|---------|------------|
| **Hecho** | Dato verificable en una fuente primaria o fiable | «El BCV publicó una tasa oficial de X Bs/USD el 2026-10-05» | 1 fuente, fecha de captura, enlace |
| **Rango entre fuentes** | Valores distintos de ≥2 fuentes para el mismo indicador | «Brecha entre oficial y paralelo: X–Y %» | ≥2 fuentes, mínimo/máximo, enlaces a todas |
| **Hipótesis** | Interpretación o inferencia del equipo | «La brecha podría ampliarse si…» | Premisas explícitas, nivel de confianza, qué la refutaría |

5. **Qué cambió vs. la semana anterior** (diff estructurado).
6. **Notas metodológicas y correcciones**.
7. **Fuentes** (lista completa con fecha de captura).

---

## 5. Modelo de datos conceptual (sin implementación)

Entidades mínimas que el MVP debe poder expresar:

- **Fuente**: nombre, tipo (oficial / multilateral / ONG / prensa / privada / dato abierto), URL base, licencia, frecuencia, fiabilidad declarada.
- **Observación**: indicador, valor, unidad, fecha del dato, **fecha de captura**, fuente, URL exacta, hash/snapshot opcional.
- **Afirmación**: texto, tipo (hecho / rango / hipótesis), observaciones asociadas, confianza (solo hipótesis).
- **Edición**: semana ISO, estado (borrador / revisada / publicada), lista de afirmaciones, changelog.
- **Corrección**: edición afectada, qué cambió, motivo, fecha.

Regla transversal: **ninguna observación existe sin fuente, fecha de captura y URL**.

---

## 6. MVP — 30 días

**Objetivo del MVP**: publicar **4 ediciones semanales consecutivas** con trazabilidad completa, datos descargables y un sitio público mínimo pero de calidad institucional.

### Alcance funcional
- **Sitio público** con: portada con la última edición, archivo de ediciones, página por edición, página de metodología, página de fuentes, página de datos/descargas, página «Acerca de».
- **Datos abiertos**: JSON/CSV derivados por edición y series acumuladas en `data/`.
- **Indicadores iniciales (acotados)**:
  - FX: tasa oficial BCV vs. al menos 2 referencias alternativas (rango entre fuentes).
  - Inflación: última cifra publicada y fuente alternativa/estimación, con rezago explícito.
  - Energía: producción/exportaciones petroleras y estado del suministro eléctrico (indicador cualitativo con fuente).
  - Sanciones/OFAC: cambios en licencias generales y designaciones relevantes (fuente primaria: OFAC/Treasury).
  - Fintech/pagos, e-commerce, infraestructura digital: **1–2 señales cualitativas citadas por edición** (no series cuantitativas aún).
- **Validación**: esquema que rechaza cifras sin fuente/fecha/enlace; chequeo de enlaces.
- **Repo público listo**: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, CITATION.cff, CI verde.

### Plan por semanas
| Semana | Foco | Entregable verificable |
|--------|------|------------------------|
| **1** | Fundamentos: metodología, catálogo de fuentes, esquema de datos, repo público con documentos de comunidad | Metodología v1 publicada; ≥15 fuentes catalogadas con licencia; edición 0 (piloto) en Markdown |
| **2** | Pipeline mínimo y validación: captura/ingreso de observaciones, generación de JSON/CSV, CI | Edición 1 publicada; CI ejecuta lint, tipos, tests y build |
| **3** | Sitio público: portada, archivo, edición, fuentes, descargas; diseño institucional | Sitio desplegado con ediciones 1–2; accesibilidad básica verificada |
| **4** | Endurecimiento y lanzamiento: correcciones, métricas de calidad, difusión inicial | Ediciones 3–4; informe de calidad del dato; anuncio público |

### Decisiones técnicas que el MVP debe respetar (sin detallarlas aquí)
- Monorepo con `apps/web`, `apps/api`, `packages/schema`, `data/`, `content/radar/`.
- **Fuente de verdad = Markdown + JSON/CSV versionados en Git.** La API no es requisito de lanzamiento: **el MVP puede salir como sitio estático + JSON**. La API (FastAPI) se incorpora cuando haya un caso de uso que lo justifique (consultas, filtrado, series).
- Esquema compartido como contrato único entre contenido, validación y frontend.

### Definición de «terminado» del MVP
- [ ] 4 ediciones consecutivas publicadas a tiempo.
- [ ] 100 % de las cifras con fuente, fecha de captura y enlace (validado automáticamente).
- [ ] Cada afirmación etiquetada (hecho / rango / hipótesis).
- [ ] Datos descargables y metodología pública.
- [ ] Repo con documentación de comunidad y licencias completas, CI en verde.
- [ ] Sitio desplegado y legible en móvil.

---

## 7. Métricas de calidad del dato

La calidad se mide, se publica y se audita. Objetivos para el MVP:

| Métrica | Definición | Objetivo MVP |
|---------|------------|--------------|
| **Cobertura de citación** | % de cifras con fuente + fecha de captura + URL | **100 %** (bloqueante) |
| **Enlaces vivos** | % de URLs que responden correctamente al publicar | ≥ 98 % |
| **Archivado de evidencia** | % de fuentes críticas con copia/archivo (p. ej. Wayback) | ≥ 80 % |
| **Frescura** | Antigüedad del dato respecto a la fecha de edición, por indicador | Dentro del umbral declarado por indicador; si no, se marca «desactualizado» |
| **Multiplicidad de fuentes** | % de indicadores clave con ≥2 fuentes independientes | ≥ 70 % (FX: 100 %) |
| **Etiquetado epistémico** | % de afirmaciones clasificadas (hecho/rango/hipótesis) | **100 %** |
| **Tasa de corrección** | Correcciones post-publicación por edición | Registrar todas; meta: ≤ 1 por edición, con respuesta < 72 h |
| **Reproducibilidad** | % de series derivadas regenerables desde las observaciones | 100 % |
| **Puntualidad** | Ediciones publicadas en la ventana comprometida | ≥ 90 % |
| **Transparencia de discrepancias** | Discrepancias entre fuentes mostradas, no ocultas | 100 % de los casos detectados |

### Reglas de calidad
- Se documenta el **rezago** de cada indicador (p. ej. inflación oficial con meses de retraso).
- Las **unidades y bases** (Bs/USD, % mensual, año base) se declaran siempre.
- Cuando hay incertidumbre o ausencia de dato: se publica «sin dato disponible», nunca una estimación sin etiqueta.
- Las correcciones se publican en la edición y en el historial; no se reescribe en silencio.
- Cada fuente tiene una ficha: tipo, sesgo/limitaciones conocidos, licencia y frecuencia.

### Métricas de producto (secundarias, privacidad primero)
- Ediciones leídas, descargas de datasets, citas/enlaces entrantes, estrellas/forks y contribuciones externas. Analítica sin cookies ni identificadores personales.

---

## 8. Criterios de «no hacer»

Regla general: **si algo no mejora la trazabilidad, la claridad o la reutilización del dato, no entra**.

### No hacer (MVP y mientras no se revise este documento)
1. **No publicar cifras sin fuente, fecha de captura y enlace.** Sin excepciones, ni «de memoria» ni «de contactos».
2. **No mezclar hecho con opinión.** Si no es verificable, es hipótesis y se etiqueta.
3. **No usar una única fuente para FX** ni presentar una tasa como «la verdadera».
4. **No construir chatbot, búsqueda semántica ni resúmenes generados sin revisión humana publicados como hechos.** Si se usa IA como apoyo editorial, la edición final la revisa y firma una persona y se documenta el uso en la metodología.
5. **No hacer scraping que viole términos de servicio, robots.txt o paywalls.** Se prioriza API, datos abiertos o ingreso manual citado.
6. **No redistribuir contenido protegido** (textos de prensa completos, datos con licencia restrictiva). Se enlaza y se resume con cita breve.
7. **No ofrecer recomendaciones de inversión, ni precios objetivo ni señales de trading.**
8. **No construir cuentas de usuario, comentarios, newsletters propios con tracking ni monetización** en el MVP.
9. **No sobreingeniería de infraestructura**: sin Kubernetes, sin microservicios, sin colas, sin base de datos gestionada hasta que haya una necesidad medida.
10. **No añadir dominios o indicadores nuevos** hasta cumplir las métricas de calidad de los existentes durante 4 semanas.
11. **No usar librerías de componentes genéricas sin personalizar** ni estética de plantilla (gradientes púrpura, tarjetas vacías, métricas decorativas).
12. **No incorporar contenido, datos, código ni marca de empleos previos del autor.** Exclusión total de cualquier IP ajena.
13. **No tomar posición política ni usar lenguaje cargado.** Descripción neutral y precisa.
14. **No almacenar datos personales ni secretos en el repositorio.** Política de seguridad y escaneo de secretos desde el primer commit.
15. **No sobreprometer cadencia.** Si una semana no hay material verificable suficiente, se publica una edición reducida con aviso, no relleno.

### Criterio de salida para revisar los «no hacer»
Se reabre una restricción solo si: (a) existe una necesidad de usuario documentada, (b) hay un plan para preservar los principios de trazabilidad y (c) se registra la decisión en `docs/decisions/` (ADR).

---

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Fuentes oficiales irregulares o inaccesibles | Huecos en series | Declarar rezago; archivar capturas; fuentes alternativas etiquetadas |
| Datos paralelos de FX con baja verificabilidad | Pérdida de credibilidad | Mostrar siempre como rango entre fuentes, nunca como cifra única |
| Percepción de sesgo político | Pérdida de confianza | Lenguaje neutro, metodología pública, correcciones visibles |
| Cambios legales/regulatorios sobre publicación | Riesgo legal | Solo fuentes públicas; aviso de no asesoría; revisión de licencias |
| Fatiga del mantenedor único | Ediciones irregulares | Alcance mínimo; edición reducida permitida; automatizar captura/validación, no el juicio |
| Alcance excesivo | MVP tardío | Criterio 10 de «no hacer»; indicadores cualitativos primero |
| Cambios de licencia/ToS en fuentes | Bloqueo de redistribución | Ficha de licencia por fuente; revisión trimestral |

---

## 10. Preguntas abiertas (a resolver antes del paso técnico)

1. **Día y hora de publicación** (propuesta: lunes por la mañana, hora de Caracas; resumen de lunes a domingo anterior).
2. **Idioma**: ¿solo español en el MVP, o resumen ejecutivo bilingüe ES/EN para inversores? (Recomendación: español primero, EN como fase 2.)
3. **Firma editorial**: ¿autoría personal o marca de proyecto con revisores?
4. **Lista inicial de fuentes** y su estado de licencia.
5. **Dominio y nombre público** (`radarvenezuela.*`) y verificación de que no hay conflicto de marca.
6. **Política de uso de IA** como apoyo editorial (borrador de redacción, clasificación) y cómo se declara.
7. **Despliegue del MVP**: sitio estático en Vercel/GitHub Pages (recomendado) frente a API desde el día 1.

---

## 11. Próximos pasos propuestos

1. Validar este documento (audiencia, anti-objetivos, alcance MVP).
2. `docs/METHODOLOGY.md` y catálogo de fuentes con licencias.
3. Diseño del esquema (`packages/schema`) a partir del modelo conceptual de la sección 5.
4. Estructura del monorepo y archivos de comunidad (README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, CITATION.cff).
5. Sistema de diseño y wireframes del sitio.
