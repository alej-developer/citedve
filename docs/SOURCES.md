# Catálogo de fuentes

Catálogo inicial de fuentes **candidatas** por dominio. Una fuente solo se usa en una señal cuando su ficha
está completa (licencia revisada, rezago y limitaciones declarados). Todas las licencias figuran como
pendientes de revisión: este documento no afirma condiciones de uso que aún no se hayan verificado.

| Dominio | Fuente | Tipo | URL base | Uso previsto | Licencia |
|---------|--------|------|----------|--------------|----------|
| FX | Banco Central de Venezuela (BCV) | Oficial | <https://www.bcv.org.ve> | Tasa oficial | Por revisar |
| Inflación | Banco Central de Venezuela (BCV) | Oficial | <https://www.bcv.org.ve> | Índice de precios publicado | Por revisar |
| Inflación | Instituto Nacional de Estadística (INE) | Oficial | <https://www.ine.gob.ve> | Estadísticas oficiales | Por revisar |
| Macro | Fondo Monetario Internacional (FMI) | Multilateral | <https://www.imf.org> | Contexto y proyecciones | Por revisar |
| Macro | Banco Mundial | Multilateral | <https://data.worldbank.org> | Series macro abiertas | Por revisar |
| Energía | OPEP, Monthly Oil Market Report | Organismo internacional | <https://www.opec.org> | Producción petrolera | Por revisar |
| Energía | U.S. EIA | Oficial (EE. UU.) | <https://www.eia.gov> | Producción, exportaciones | Por revisar |
| Sanciones | OFAC, U.S. Treasury | Oficial (EE. UU.) | <https://ofac.treasury.gov> | Licencias generales y designaciones | Por revisar |
| Fintech/Pagos | SUDEBAN | Oficial | <https://www.sudeban.gob.ve> | Regulación bancaria y de pagos | Por revisar |
| Infra. digital | CONATEL | Oficial | <https://www.conatel.gob.ve> | Telecomunicaciones | Por revisar |
| Infra. digital | UIT (ITU DataHub) | Multilateral | <https://datahub.itu.int> | Conectividad | Por revisar |
| Infra. digital | Cloudflare Radar | Privada (datos abiertos) | <https://radar.cloudflare.com> | Tráfico e interrupciones | Por revisar |
| Archivo | Internet Archive (Wayback Machine) | Archivo | <https://web.archive.org> | `archive_url` de evidencia | N/A |

## Ficha mínima de cada fuente

| Campo | Contenido |
|-------|-----------|
| Tipo | oficial / multilateral / ONG / prensa / privada / dato abierto |
| Licencia y redistribución | Qué se puede copiar, citar o enlazar |
| Frecuencia y rezago | Cada cuánto publica y con qué retraso |
| Limitaciones | Sesgos, cambios metodológicos, cobertura |
| Método de captura | API, descarga abierta o ingreso manual citado |

## Criterios de incorporación

1. Pública y accesible sin saltarse paywalls ni términos de servicio.
2. Enlace estable al dato exacto.
3. Metodología conocida o limitaciones declaradas.
4. Para FX, siempre ≥ 2 fuentes y presentación como rango; las referencias de mercado paralelo se
   incorporan solo con la metodología documentada (ver `ROADMAP.md`).
