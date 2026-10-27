import assert from "node:assert/strict";
import { test } from "node:test";

import { isStale } from "./fxFreshness.ts";

test("ocho días exactos no marcan desactualizado", () => {
  assert.equal(isStale("2026-10-08", "2026-10-16", 8), false);
});

test("más de ocho días marca desactualizado", () => {
  assert.equal(isStale("2026-10-07", "2026-10-16", 8), true);
});

test("el mismo día y un corte futuro siguen vigentes", () => {
  assert.equal(isStale("2026-10-16", "2026-10-16"), false);
  assert.equal(isStale("2026-10-23", "2026-10-16"), false);
});
