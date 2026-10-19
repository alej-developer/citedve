import fs from "node:fs";
import path from "node:path";

import { FX_NOTICE, FRESHNESS_MAX_DAYS } from "@/lib/fxView";

const ROOT = path.resolve(process.cwd(), "..", "..");

export interface FxCell {
  status: string;
  as_of_date: string;
  date_basis: string;
  operation_date?: string | null;
  unit: string;
  value: number | null;
  value_as_published: string | null;
  notes?: string | null;
  retraction_reason?: string | null;
  source: {
    name: string;
    url: string;
    locator?: string | null;
    accessed_at: string;
    archive_url?: string | null;
    publisher_id: string;
    upstream_id?: string | null;
  };
}

export interface FxBankRow {
  institution: { id: string; name: string; kind: string };
  compra: FxCell | null;
  venta: FxCell | null;
  discrepancia: boolean;
}

export interface FxDispersion {
  min: number;
  max: number;
  amplitud: number;
  n: number;
}

export interface FxSourceRef {
  name: string;
  url: string;
  archive_url?: string | null;
  accessed_at: string;
  publisher_id: string;
  upstream_id?: string | null;
  value: number;
}

export interface FxP2PPublished {
  estado: "publicado";
  side: string;
  unit: string;
  min: number;
  max: number;
  mediana: number;
  n_fuentes: number;
  n_editores: number;
  limitacion_editor_unico: boolean;
  fuentes: FxSourceRef[];
}

export type FxP2P = { estado: "sin_dato" } | FxP2PPublished;

export interface FxGapPoint {
  label: string;
  side: string;
  official_label: string;
  official: number;
  parallel_label: string;
  parallel: number;
  text: string;
}

export interface FxLatest {
  schema_version: string;
  edition: null | {
    id: string;
    cutoff_date: string;
    status: string;
    p2p_status: "publicado" | "sin_dato";
    notes?: string | null;
  };
  notice: string;
  freshness_max_days: number;
  retracted_banner?: string | null;
  official?: { compra: FxCell | null; venta: FxCell | null };
  banks?: FxBankRow[];
  dispersion?: { compra: FxDispersion | null; venta: FxDispersion | null };
  p2p?: FxP2P;
  gaps?: FxGapPoint[] | null;
}

export function emptyFxLatest(): FxLatest {
  return {
    schema_version: "0.1.0",
    edition: null,
    notice: FX_NOTICE,
    freshness_max_days: FRESHNESS_MAX_DAYS,
  };
}

export function loadFxLatest(): FxLatest {
  try {
    const file = path.join(ROOT, "data", "fx", "latest.json");
    return JSON.parse(fs.readFileSync(file, "utf-8")) as FxLatest;
  } catch {
    return emptyFxLatest();
  }
}
