import type { FxCell, FxDispersion, FxP2PPublished } from "@/lib/fxLatest";

export const FX_NOTICE =
  "Foto semanal, no cotización en vivo. Información, no asesoramiento.";

export const FRESHNESS_MAX_DAYS = 8;

export const P2P_EMPTY =
  "Sin dato disponible: menos de 2 fuentes independientes con fecha para este corte.";

export const GAP_UNAVAILABLE = "La brecha no se calcula con una sola tasa.";

export const SINGLE_PUBLISHER =
  "Limitación de editor único: estas fuentes las publica un solo editor.";

export const USDT_NOTE =
  "USDT no es USD; es una referencia de mercado entre particulares, no una tasa de ejecución.";

export const BANK_FOOTNOTE =
  "El BCV publica solo algunas instituciones por día; la lista no es exhaustiva.";

export const AGGREGATE_NOTE = "agregado publicado por el BCV, no es un banco";

export const SOURCE_DISCREPANCY = "Así lo publica la fuente";

export const GAP_FORMULA = "(P2P − BCV) / BCV";

export function formatRate(value: number): string {
  if (!Number.isFinite(value)) return "n/d";
  const trimmed = value.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
  return trimmed.replace(".", ",");
}

export function sideText(cell: FxCell | null): string {
  if (!cell || cell.status !== "published" || cell.value == null || cell.value_as_published == null) {
    const reason = cell?.retraction_reason ? `: ${cell.retraction_reason}` : "";
    return `Retirado${reason}`;
  }
  return `${cell.value_as_published} ${cell.unit}`;
}

export function dispersionLine(side: string, value: FxDispersion | null): string {
  if (!value) return `${side}: sin dato de dispersión.`;
  const span = `Entre ${formatRate(value.min)} y ${formatRate(value.max)} Bs/USD`;
  return `${side}: ${span} (amplitud ${formatRate(value.amplitud)}; ${value.n} instituciones).`;
}

export function p2pSummary(p2p: FxP2PPublished): string {
  const span = `Entre ${formatRate(p2p.min)} y ${formatRate(p2p.max)} Bs/USDT`;
  return `${span} · mediana ${formatRate(p2p.mediana)} · ${p2p.n_fuentes} fuentes`;
}

export function operationDate(cell: FxCell | null): string | null {
  return cell?.operation_date ?? null;
}
