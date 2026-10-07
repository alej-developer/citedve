/**
 * Tipos del contrato de datos. La fuente de verdad es `signals.schema.json`;
 * este archivo es su espejo TypeScript y el espejo Pydantic vive en
 * `apps/api/radar_api/models.py`. Cualquier cambio debe tocar los tres.
 */

export const SCHEMA_VERSION = "0.1.0" as const;

export const CATEGORIES = [
  "fx",
  "inflation",
  "energy",
  "sanctions",
  "fintech",
  "ecommerce",
  "digital_infra",
  "politics_risk",
  "other"
] as const;
export type Category = (typeof CATEGORIES)[number];

export const DIRECTIONS = ["up", "down", "flat", "mixed", "n/a"] as const;
export type Direction = (typeof DIRECTIONS)[number];

export const CONFIDENCE_LEVELS = ["high", "medium", "low"] as const;
export type Confidence = (typeof CONFIDENCE_LEVELS)[number];

export const STATUSES = ["published", "draft", "retracted"] as const;
export type Status = (typeof STATUSES)[number];

/** Fecha ISO `YYYY-MM-DD`. */
export type IsoDate = string;
/** Fecha ISO con hora `YYYY-MM-DDTHH:mm:ssZ`. */
export type IsoDateTime = string;

export interface Source {
  name: string;
  url: string;
  accessed_at: IsoDate;
}

export interface Signal {
  id: string;
  title: string;
  category: Category;
  summary: string;
  value_numeric?: number | null;
  value_text?: string | null;
  unit?: string | null;
  as_of_date: IsoDate;
  captured_at: IsoDateTime;
  direction: Direction;
  confidence: Confidence;
  sources: Source[];
  tags: string[];
  region: string;
  notes?: string | null;
  status: Status;
}

export interface SignalsDocument {
  schema_version: string;
  signals: Signal[];
}

export interface LatestDocument {
  schema_version: string;
  edition: IsoDate | null;
  signals: Signal[];
}
