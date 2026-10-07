import type { ClaimType } from "@radar/schema";

const META: Record<ClaimType, { label: string; hint: string; className: string }> = {
  fact: {
    label: "Hecho",
    hint: "Verificable en una fuente",
    className: "border-fact text-fact",
  },
  range: {
    label: "Rango entre fuentes",
    hint: "Fuentes que discrepan",
    className: "border-range text-range",
  },
  hypothesis: {
    label: "Hipótesis",
    hint: "Interpretación con premisas",
    className: "border-hypothesis text-hypothesis",
  },
};

export const CLAIM_META = META;

export function ClaimBadge({ type }: { type: ClaimType }) {
  const meta = META[type];
  return (
    <span
      className={`inline-block border px-2 py-0.5 font-mono text-[11px] uppercase tracking-wider ${meta.className}`}
      title={meta.hint}
    >
      {meta.label}
    </span>
  );
}
