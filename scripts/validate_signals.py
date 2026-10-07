"""Valida `data/signals.json` contra el JSON Schema y reglas de integridad del repo.

Uso:  uv run python scripts/validate_signals.py
Sale con código 1 si hay errores.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "schema" / "signals.schema.json"
SIGNALS_PATH = ROOT / "data" / "signals.json"
CONTENT_DIR = ROOT / "content" / "radar"
EDITION_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_errors(
    signals_path: Path = SIGNALS_PATH,
    schema_path: Path = SCHEMA_PATH,
    content_dir: Path = CONTENT_DIR,
) -> list[str]:
    errors: list[str] = []
    document = load_json(signals_path)
    validator = Draft202012Validator(load_json(schema_path))
    for err in sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(p) for p in err.absolute_path) or "<raíz>"
        errors.append(f"schema: {location}: {err.message}")
    if errors:
        return errors

    seen: set[str] = set()
    for signal in document["signals"]:
        sid = signal["id"]
        if sid in seen:
            errors.append(f"integridad: id duplicado '{sid}'")
        seen.add(sid)
        if signal["claim_type"] == "range":
            urls = [s["url"] for s in signal["sources"]]
            if len(set(urls)) < 2:
                errors.append(f"integridad: '{sid}' exige 2 fuentes con URL distinta")
            if signal["range"]["min"] > signal["range"]["max"]:
                errors.append(f"integridad: '{sid}' tiene range.min > range.max")
        for source in signal["sources"]:
            if source["captured_at"] > signal["edition"]:
                errors.append(f"integridad: '{sid}' captura posterior a la edición")
        if not (content_dir / f"{signal['edition']}.md").exists():
            errors.append(
                f"integridad: '{sid}' referencia edición sin content/radar/{signal['edition']}.md"
            )

    for path in sorted(content_dir.glob("*.md")):
        if path.name.lower() == "readme.md" or path.name.startswith("_"):
            continue
        if not EDITION_FILE.match(path.name):
            errors.append(f"contenido: '{path.name}' no sigue el formato YYYY-MM-DD.md")
    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        print(f"ERROR {len(errors)} error(es) en data/signals.json", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        return 1
    count = len(load_json(SIGNALS_PATH)["signals"])
    print(f"OK data/signals.json válido ({count} señales)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
