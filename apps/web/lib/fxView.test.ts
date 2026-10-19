import assert from "node:assert/strict";
import { test } from "node:test";

import type { FxCell, FxP2PPublished } from "./fxLatest.ts";
import {
  FX_NOTICE,
  GAP_FORMULA,
  P2P_EMPTY,
  dispersionLine,
  formatRate,
  p2pSummary,
  sideText,
} from "./fxView.ts";

function cell(overrides: Partial<FxCell> = {}): FxCell {
  return {
    status: "published",
    as_of_date: "2026-10-16",
    date_basis: "fecha_indicador",
    unit: "VES/USD",
    value: 110,
    value_as_published: "110,00",
    source: {
      name: "Fuente sintética",
      url: "https://www.bcv.org.ve/tasas-informativas-sistema-bancario",
      accessed_at: "2026-10-16T18:00:00Z",
      publisher_id: "bcv",
    },
    ...overrides,
  };
}

test("la fila publicada cita el texto de la fuente y la unidad", () => {
  assert.equal(sideText(cell()), "110,00 VES/USD");
  assert.equal(FX_NOTICE.includes("no cotización en vivo"), true);
  assert.equal(GAP_FORMULA, "(P2P − BCV) / BCV");
  assert.match(P2P_EMPTY, /menos de 2 fuentes/);
});

test("una fila retirada oculta el valor", () => {
  const text = sideText(
    cell({
      status: "retracted",
      value: 999,
      value_as_published: "999,00",
      retraction_reason: "motivo sintético",
    }),
  );
  assert.match(text, /Retirado: motivo sintético/);
  assert.equal(text.includes("999"), false);
});

test("la dispersión no nombra instituciones", () => {
  const line = dispersionLine("Compra", { min: 110, max: 130.5, amplitud: 20.5, n: 3 });
  assert.equal(line, "Compra: Entre 110 y 130,5 Bs/USD (amplitud 20,5; 3 instituciones).");
  assert.equal(formatRate(100), "100");
});

test("el resumen P2P etiqueta mínimo, máximo y mediana", () => {
  const p2p: FxP2PPublished = {
    estado: "publicado",
    side: "compra",
    unit: "VES/USDT",
    min: 150,
    max: 160,
    mediana: 155,
    n_fuentes: 2,
    n_editores: 1,
    limitacion_editor_unico: true,
    fuentes: [],
  };
  assert.equal(p2pSummary(p2p), "Entre 150 y 160 Bs/USDT · mediana 155 · 2 fuentes");
});
