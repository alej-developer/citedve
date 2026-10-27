/**
 * Espejo TypeScript de `fx_observations.schema.json`.
 * No forma parte del contrato de señales.
 */

export const FX_SCHEMA_VERSION = "0.1.0" as const;

export const FX_INDICATORS = [
  "tasa_oficial_bcv",
  "tasa_informativa_banco",
  "p2p_referencia",
] as const;
export type FxIndicator = (typeof FX_INDICATORS)[number];

export const FX_INSTITUTION_KINDS = [
  "banco_central",
  "banco",
  "agregado_fuente",
  "mercado_p2p",
] as const;
export type FxInstitutionKind = (typeof FX_INSTITUTION_KINDS)[number];

export const FX_SIDES = ["compra", "venta", "referencia"] as const;
export type FxSide = (typeof FX_SIDES)[number];

export const FX_UNITS = ["VES/USD", "VES/USDT"] as const;
export type FxUnit = (typeof FX_UNITS)[number];

export const FX_DATE_BASES = [
  "fecha_valor",
  "fecha_operacion",
  "fecha_indicador",
  "captura_archivada",
] as const;
export type FxDateBasis = (typeof FX_DATE_BASES)[number];

export const FX_EDITION_STATUSES = ["draft", "published", "retracted"] as const;
export type FxEditionStatus = (typeof FX_EDITION_STATUSES)[number];

export const FX_P2P_STATUSES = ["publicado", "sin_dato"] as const;
export type FxP2pStatus = (typeof FX_P2P_STATUSES)[number];

export const FX_OBSERVATION_STATUSES = ["published", "retracted"] as const;
export type FxObservationStatus = (typeof FX_OBSERVATION_STATUSES)[number];

export interface FxEdition {
  id: string;
  cutoff_date: string;
  status: FxEditionStatus;
  p2p_status: FxP2pStatus;
  retraction_reason?: string | null;
  notes?: string | null;
}

export interface FxInstitution {
  id: string;
  name: string;
  kind: FxInstitutionKind;
}

export interface FxSource {
  name: string;
  publisher_id: string;
  upstream_id?: string;
  url: string;
  locator?: string | null;
  accessed_at: string;
  archive_url?: string;
  sha256?: string;
  license: string;
}

export interface FxObservation {
  id: string;
  edition: string;
  indicator: FxIndicator;
  institution: FxInstitution;
  side: FxSide;
  value: number;
  value_as_published: string;
  unit: FxUnit;
  as_of_date: string;
  date_basis: FxDateBasis;
  operation_date?: string;
  status: FxObservationStatus;
  retraction_reason?: string | null;
  source: FxSource;
  notes?: string | null;
}

export interface FxObservationsDocument {
  schema_version: typeof FX_SCHEMA_VERSION;
  editions: FxEdition[];
  observations: FxObservation[];
}
