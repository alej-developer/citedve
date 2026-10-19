/** Umbral de frescura del panel: más de 8 días desde el corte. */

export const FRESHNESS_MAX_DAYS = 8;

function utcDay(iso: string): number {
  const [year, month, day] = iso.slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

/** `true` cuando `hoy − corte` es mayor que `maxDays`. Ocho días exactos sigue vigente. */
export function isStale(cutoff: string, today: string, maxDays = FRESHNESS_MAX_DAYS): boolean {
  const days = (utcDay(today) - utcDay(cutoff)) / 86_400_000;
  return days > maxDays;
}
