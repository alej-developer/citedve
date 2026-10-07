import fs from "node:fs";
import path from "node:path";
import type { LatestDocument } from "@radar/schema";

/** `data/latest.json` en la raíz del monorepo; se lee en build (sitio estático). */
export function loadLatest(): LatestDocument {
  const file = path.resolve(process.cwd(), "..", "..", "data", "latest.json");
  return JSON.parse(fs.readFileSync(file, "utf-8")) as LatestDocument;
}
