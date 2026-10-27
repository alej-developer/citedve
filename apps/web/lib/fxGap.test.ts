import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { computeFxGap } from "./fxGap.ts";

const casesPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../../packages/schema/fixtures/fx_gap_cases.json",
);
const gapCases = JSON.parse(fs.readFileSync(casesPath, "utf8")) as {
  official: number;
  parallel: number;
  label: string;
}[];

test("el fixture compartido coincide con computeFxGap", () => {
  for (const row of gapCases) {
    assert.equal(computeFxGap(row.official, row.parallel).label, row.label);
  }
});

test("el porcentaje es (paralelo - oficial) / oficial", () => {
  const view = computeFxGap(36, 39.5);
  assert.equal(view.comparable, true);
  assert.equal(view.label, "9.7%");
});

test("la barra refleja la brecha y no queda fija en 50/50", () => {
  const view = computeFxGap(36, 39.5);
  assert.equal(view.baseWidth, "91.1392%");
  assert.equal(view.gapWidth, "8.8608%");
  assert.equal(view.gapX, "91.1392%");
  assert.notEqual(view.baseWidth, "50.0000%");
  assert.notEqual(view.gapWidth, "50.0000%");
});

test("50/50 solo cuando una tasa es el doble de la otra", () => {
  const doubled = computeFxGap(100, 200);
  assert.equal(doubled.label, "100.0%");
  assert.equal(doubled.baseWidth, "50.0000%");
  assert.equal(doubled.gapWidth, "50.0000%");
});

test("tasas iguales llenan la barra y la brecha es cero", () => {
  const view = computeFxGap(873.867, 873.867);
  assert.equal(view.label, "0.0%");
  assert.equal(view.baseWidth, "100.0000%");
  assert.equal(view.gapWidth, "0.0000%");
});

test("si el paralelo queda por debajo del oficial, el porcentaje es negativo y la barra muestra la diferencia", () => {
  const view = computeFxGap(200, 100);
  assert.equal(view.label, "-50.0%");
  assert.equal(view.baseWidth, "50.0000%");
  assert.equal(view.gapWidth, "50.0000%");
});

test("tasas no positivas o no finitas no inventan una barra", () => {
  for (const [official, parallel] of [
    [0, 100],
    [-1, 10],
    [10, 0],
    [Number.NaN, 10],
    [10, Number.POSITIVE_INFINITY],
  ] as const) {
    const view = computeFxGap(official, parallel);
    assert.equal(view.comparable, false);
    assert.equal(view.label, "n/d");
    assert.equal(view.baseWidth, "0%");
    assert.equal(view.gapWidth, "0%");
  }
});
