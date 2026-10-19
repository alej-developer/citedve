# Catálogo de fuentes

Lista de fuentes legítimas para **CitedVE**. El radar se construye exclusivamente con información de las fuentes documentadas aquí. Prohibido inventar cifras. Si no hay fuente, no hay señal. Las opiniones están excluidas; solo usamos reportes de datos duros u observables.

| Dominio | Fuente | Tipo | Descripción | URL Base |
|---------|--------|------|-------------|----------|
| FX / Macro | Banco Central de Venezuela (BCV) | Oficial | Tasa oficial y datos macro base | <https://www.bcv.org.ve> |
| Sanciones / Legal | OFAC, U.S. Treasury | Oficial (EE. UU.) | Licencias, designaciones | <https://ofac.treasury.gov/recent-actions> |
| Migración / Humanitario | R4V (Plataforma Regional de Coord.) | Multilateral | Flujos migratorios y datos de contexto | <https://www.r4v.info> |
| Inflación / Economía | OVF (Observatorio Venezolano de Finanzas) | ONG | Datos alternativos de inflación y actividad económica | <https://observatoriodefinanzas.com> |
| Social / Encuestas | ENCOVI | Académico | Condiciones de vida y pobreza multidimensional | <https://proyectoencovi.com> |
| Canasta Básica | Cenda / Cendas | ONG | Costo de la canasta alimentaria / básica | <https://cendasfvm.org> |
| General / Negocios | Reuters / Bloomberg | Prensa seria | Hechos duros y reportes de mercado (excluyendo piezas de opinión) | <https://www.reuters.com>, <https://www.bloomberg.com> |

## Criterios de incorporación

1. Toda señal `published` exige ≥ 1 source con URL en vivo o archivada.
2. Nivel de `confidence`:
   - `high`: Fuente primaria oficial (BCV, OFAC, etc.)
   - `medium`: Prensa seria o entidades independientes reconocidas (Reuters, Bloomberg, ENCOVI, OVF)
   - `low`: Estimados puntuales sin publicación metodológica detallada, pero capturados como señal
3. Prohibido mezclar hechos puros con opinión.

## Panel de tasas (FX)

Alcance del [ADR-0001](decisions/ADR-0001-panel-tasas.md). La captura es manual y citada. No hay captura automática ni scraping que vaya contra los términos de un sitio. No se crean instantáneas de archivo desde este repositorio. Cada cifra publicada lleva la URL exacta del dato.

Dominios permitidos en las observaciones FX: `www.bcv.org.ve`, `www.usdt.com.ve` y `web.archive.org`. Cualquier otro dominio se añade en un PR que revise sus términos.

### Fuentes admitidas

| Fuente | Qué se cita | URL del dato | Términos |
|--------|-------------|--------------|----------|
| BCV, tipo de cambio de referencia SMC | Tasa oficial USD en Bs, compra y venta, por hoja del libro trimestral | Índice: <https://www.bcv.org.ve/estadisticas/tipo-cambio-de-referencia-smc>. Libro: `https://www.bcv.org.ve/sites/default/files/EstadisticasGeneral/2_1_2{a,b,c,d}{AA}_smc.xls` | <https://www.bcv.org.ve/terminos-condiciones>: se puede reproducir la información sin fines de lucro citando la fuente. La propia página advierte que no debe usarse como fundamento de una decisión. `robots.txt` fija `Crawl-delay: 10` y no veta `/estadisticas/` ni `/sites/default/files/` |
| BCV, tasas informativas del sistema bancario | Tasa por institución y la fila agregada «Otras Instituciones» | <https://www.bcv.org.ve/tasas-informativas-sistema-bancario> con el filtro de fecha en la query | Los mismos términos del BCV. La lista de un día no es exhaustiva |
| usdt.com.ve | Mediana P2P de Binance y de Bybit, en VES/USDT | Páginas con fecha solo si se cita una instantánea ya archivada (`archive_url`). El CSV CC BY está en <https://www.usdt.com.ve/datos> | El dataset declara CC BY 4.0. `robots.txt` veta `/api/`. Que la licencia del dataset cubra las páginas vivas no está verificado; por eso la página viva no basta y hace falta una URL archivada con fecha |

La tasa oficial usa la fecha de operación del libro SMC (`date_basis: fecha_operacion`). La fecha valor puede ser posterior y no fija el corte.

### Descartes (no entran en el MVP)

| Candidato | Motivo |
|-----------|--------|
| Binance P2P como fuente directa | `robots.txt` veta `/bapi/`. No hay página con fecha. Un listado de anuncios puede mostrar alias de terceros |
| Bybit P2P como fuente directa | No hay página con fecha |
| monitordedivisavenezuela.com | Los términos prohíben la reproducción sin autorización escrita y el uso de bots o scrapers |
| Exchange Monitor (exchangemonitor.net) | El uso permitido es personal; no autoriza copiar ni distribuir |
| CriptoYa (criptoya.com) | No autoriza ofrecer sus datos en otros medios. Los enlaces pueden llevar referidos |
| PitbullChain (pitbullchain.com) | Enlaces de afiliado y orientación a bots de trading |
| Yadio (yadio.io) | Términos no revisados. Fuera del MVP |
| El Dorado (eldorado.io) | Es un operador, no una referencia neutral. Fuera del MVP |

También se rechaza cualquier URL con `/bapi/` o con parámetros de afiliado (`ref`, `aff`, `utm_`, `referral`, `affiliate`).

### Decisiones del dueño (2026-10-19)

Las mismas tres decisiones están en el ADR-0001.

1. **Independencia P2P.** Las medianas de Binance y de Bybit publicadas por usdt.com.ve cuentan como 2 fuentes para la regla «≥ 2 fuentes». La independencia se mide por `upstream_id` distinto, aunque el editor (`publisher_id`) sea el mismo. Limitación de editor único: hay un solo editor. El panel lo dice de forma explícita. No son dos editores independientes.
2. **Corte y frescura.** El corte semanal es el viernes. La fecha que manda para la tasa oficial del BCV es la fecha de operación. Se muestra «desactualizado» cuando el corte tiene más de 8 días (`hoy − cutoff_date > 8`).
3. **Brecha.** Se muestra la brecha frente al mínimo, al máximo y a la mediana P2P, cada una con su etiqueta.
