# Política de seguridad

## Versiones con soporte

Solo la rama `main`. El proyecto está en fase pre-1.0.

## Cómo reportar una vulnerabilidad

**No abras un issue público.** Usa el reporte privado de GitHub:
<https://github.com/alej-developer/radar-venezuela/security/advisories/new>

Incluye pasos para reproducir, impacto estimado y versión/commit afectado. Responderemos con un
acuse de recibo en un plazo objetivo de 5 días hábiles y coordinaremos la divulgación contigo.

## Alcance

- Código de `apps/api`, `apps/web` y `scripts/`.
- Configuración de CI/CD.
- Secretos o datos personales expuestos por error en el repositorio.

## Fuera de alcance

- Errores en cifras o fuentes (usa un issue de corrección de datos).
- Vulnerabilidades de servicios de terceros citados.

## Principios

El proyecto no almacena datos personales ni secretos en el repositorio, y solo usa fuentes públicas.
