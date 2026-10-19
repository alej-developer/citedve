import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");

const BANNED = [/mejor/i, /conviene/i, /recomend/i, /oferta/i, /ahorra/i, /compra aquí/i, /\bgana\b/i];
const AFFILIATE = [/[?&]ref=/, /[?&]aff=/, /utm_/, /[?&]referral=/, /affiliate/i];

function walk(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return walk(full);
    if (entry.name.endsWith(".test.ts")) return [];
    return [full];
  });
}

test("latest.json mantiene el orden alfabético y los agregados al final", () => {
  const latest = JSON.parse(fs.readFileSync(path.join(root, "data/fx/latest.json"), "utf8")) as {
    banks?: { institution: { name: string; kind: string } }[];
  };
  const banks = latest.banks ?? [];
  const names = banks
    .filter((row) => row.institution.kind !== "agregado_fuente")
    .map((row) => row.institution.name);
  const sorted = [...names].sort((a, b) => a.localeCompare(b, "es", { sensitivity: "accent" }));
  assert.deepEqual(names, sorted);
  const aggregateAt = banks.findIndex((row) => row.institution.kind === "agregado_fuente");
  if (aggregateAt >= 0) {
    assert.ok(banks.slice(aggregateAt).every((row) => row.institution.kind === "agregado_fuente"));
  }
});

test("la página y los componentes FX no tienen ranking ni afiliados", () => {
  const files = [
    ...walk(path.join(root, "apps/web/app/fx")),
    ...walk(path.join(root, "apps/web/components/fx")),
    path.join(root, "apps/web/components/FxGapMeter.tsx"),
    path.join(root, "apps/web/lib/fxView.ts"),
    path.join(root, "apps/web/lib/fxFreshness.ts"),
    path.join(root, "apps/web/lib/fxLatest.ts"),
  ];
  for (const file of files) {
    const source = fs.readFileSync(file, "utf8");
    for (const pattern of [...BANNED, ...AFFILIATE]) {
      assert.equal(pattern.test(source), false, `${file} coincide con ${pattern}`);
    }
  }
});

test("la tabla de bancos no acepta orden ni resaltado", () => {
  const source = fs.readFileSync(
    path.join(root, "apps/web/components/fx/BankRateTable.tsx"),
    "utf8",
  );
  assert.equal(/\bsort\b/i.test(source), false);
  assert.equal(/highlight/i.test(source), false);
  assert.match(source, /rows: FxBankRow\[\]/);
});
