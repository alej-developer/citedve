"""Deriva `data/signals.csv` y `data/latest.json` desde `data/signals.json`.

Uso:
    uv run python scripts/build_data.py          # escribe los derivados
    uv run python scripts/build_data.py --check  # falla si están desactualizados (CI)

No hace ingestión: `signals.json` es la fuente de verdad y se edita por PR.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from typing import Any

from validate_signals import ROOT, SIGNALS_PATH, collect_errors, load_json

CSV_PATH = ROOT / "data" / "signals.csv"
LATEST_PATH = ROOT / "data" / "latest.json"
SCHEMA_VERSION = "0.1.0"

CSV_COLUMNS = [
    "id",
    "edition",
    "domain",
    "indicator",
    "claim_type",
    "title",
    "value",
    "unit",
    "range_min",
    "range_max",
    "observed_at",
    "confidence",
    "source_names",
    "source_urls",
    "source_captured_at",
]


def _cell(value: Any) -> str:
    return "" if value is None else str(value)


def sorted_signals(document: dict[str, Any]) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = document["signals"]
    return sorted(signals, key=lambda s: (s["edition"], s["id"]))


def render_csv(signals: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for s in signals:
        rng = s.get("range") or {}
        sources = s["sources"]
        writer.writerow(
            [
                s["id"],
                s["edition"],
                s["domain"],
                s["indicator"],
                s["claim_type"],
                s["title"],
                _cell(s.get("value")),
                _cell(s.get("unit")),
                _cell(rng.get("min")),
                _cell(rng.get("max")),
                s["observed_at"],
                _cell(s.get("confidence")),
                " | ".join(x["name"] for x in sources),
                " | ".join(x["url"] for x in sources),
                " | ".join(x["captured_at"] for x in sources),
            ]
        )
    return buffer.getvalue()


def render_latest(signals: list[dict[str, Any]]) -> str:
    edition = max((s["edition"] for s in signals), default=None)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "edition": edition,
        "signals": [s for s in signals if s["edition"] == edition],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv
    errors = collect_errors()
    if errors:
        print("ERROR signals.json inválido; ejecuta scripts/validate_signals.py", file=sys.stderr)
        return 1

    signals = sorted_signals(load_json(SIGNALS_PATH))
    outputs = {CSV_PATH: render_csv(signals), LATEST_PATH: render_latest(signals)}

    stale = [
        path
        for path, text in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != text
    ]
    if check:
        if stale:
            names = ", ".join(p.name for p in stale)
            print(
                f"ERROR derivados desactualizados: {names}. Ejecuta build_data.py", file=sys.stderr
            )
            return 1
        print("OK derivados al día")
        return 0

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK escritos {CSV_PATH.name} y {LATEST_PATH.name} ({len(signals)} señales)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
