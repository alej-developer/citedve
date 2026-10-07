/**
 * Tipos del contrato de datos. La fuente de verdad es `signals.schema.json`;
 * este archivo es su espejo TypeScript y el espejo Pydantic vive en
 * `apps/api/radar_api/models.py`. Cualquier cambio debe tocar los tres.
 */

export const SCHEMA_VERSION = "0.1.0" as const;

export const DOMAINS = [
  "fx",
  "inflation",
  "energy",
  "sanctions",
  "fintech",
  "ecommerce",
  "digital_infra",
] as const;
export type Domain = (typeof DOMAINS)[number];

export const CLAIM_TYPES = ["fact", "range", "hypothesis"] as const;
export type ClaimType = (typeof CLAIM_TYPES)[number];

export type Confidence = "low" | "medium" | "high";

/** Fecha ISO `YYYY-MM-DD`. */
export type IsoDate = string;

export interface Source {
  name: string;
  url: string;
  captured_at: IsoDate;
  published_at?: IsoDate;
  archive_url?: string;
}

export interface ValueRange {
  min: number;
  max: number;
}

export interface Signal {
  id: string;
  edition: IsoDate;
  domain: Domain;
  indicator: string;
  claim_type: ClaimType;
  title: string;
  statement: string;
  value?: number | null;
  unit?: string | null;
  range?: ValueRange;
  observed_at: IsoDate;
  sources: Source[];
  confidence?: Confidence;
  assumptions?: string[];
  falsifiers?: string[];
}

export interface SignalsDocument {
  schema_version: typeof SCHEMA_VERSION;
  signals: Signal[];
}

export interface LatestDocument {
  schema_version: typeof SCHEMA_VERSION;
  edition: IsoDate | null;
  signals: Signal[];
}
