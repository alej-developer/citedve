"""Valida `data/signals.json` contra el JSON Schema y reglas de integridad del repo.

Uso:  uv run python scripts/validate_signals.py
Sale con código 1 si hay errores.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from datetime import datetime

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "schema" / "signals.schema.json"
SIGNALS_PATH = ROOT / "data" / "signals.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_errors(
    signals_path: Path = SIGNALS_PATH,
    schema_path: Path = SCHEMA_PATH,
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
        
        if signal["status"] == "published" and len(signal.get("sources", [])) == 0:
            errors.append(f"integridad: '{sid}' está published pero no tiene sources")
            
        # Optional validation for accessed_at <= as_of_date or similar if needed.
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
