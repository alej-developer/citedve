/**
 * Brecha BCV vs P2P y anchos de la barra.
 *
 * El porcentaje es (paralelo − oficial) / oficial.
 * La barra usa la tasa mayor como 100 %: el tramo base es la tasa menor
 * y el tramo de brecha es la diferencia. Solo queda en 50/50 cuando una
 * tasa es el doble de la otra.
 */

export interface FxGapView {
  /** Texto del porcentaje, p. ej. "13.5%". "n/d" si las tasas no se pueden comparar. */
  label: string;
  /** Ancho CSS del tramo base (tasa menor / tasa mayor). */
  baseWidth: string;
  /** Ancho CSS del tramo de diferencia. */
  gapWidth: string;
  /** Posición X del tramo de diferencia. */
  gapX: string;
  comparable: boolean;
}

function percentWidth(share: number): string {
  return `${share.toFixed(4)}%`;
}

export function computeFxGap(official: number, parallel: number): FxGapView {
  const invalid =
    !Number.isFinite(official) ||
    !Number.isFinite(parallel) ||
    official <= 0 ||
    parallel <= 0;

  if (invalid) {
    return {
      label: "n/d",
      baseWidth: "0%",
      gapWidth: "0%",
      gapX: "0%",
      comparable: false,
    };
  }

  const gapPercent = ((parallel - official) / official) * 100;
  const baseShare = (Math.min(official, parallel) / Math.max(official, parallel)) * 100;
  const gapShare = 100 - baseShare;

  return {
    label: `${gapPercent.toFixed(1)}%`,
    baseWidth: percentWidth(baseShare),
    gapWidth: percentWidth(gapShare),
    gapX: percentWidth(baseShare),
    comparable: true,
  };
}
