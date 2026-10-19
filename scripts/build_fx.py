"""Deriva `data/fx/observations.csv` y `data/fx/latest.json`.

Uso:
    uv run python scripts/build_fx.py
    uv run python scripts/build_fx.py --check

Con el conjunto vacío (ninguna edición published) escribe la foto vacía.
Una edición published usa los cálculos de `radar_api.fx`.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from typing import Any

from radar_api.fx import FRESHNESS_MAX_DAYS, NOTICE, SCHEMA_VERSION, render_published_latest
from validate_fx import OBSERVATIONS_PATH, ROOT, collect_errors, load_json

CSV_PATH = ROOT / "data" / "fx" / "observations.csv"
LATEST_PATH = ROOT / "data" / "fx" / "latest.json"

CSV_COLUMNS = [
    "id",
    "edition",
    "indicator",
    "institution_id",
    "institution_name",
    "institution_kind",
    "side",
    "value",
    "value_as_published",
    "unit",
    "as_of_date",
    "date_basis",
    "operation_date",
    "status",
    "retraction_reason",
    "source_name",
    "publisher_id",
    "upstream_id",
    "url",
    "locator",
    "accessed_at",
    "archive_url",
    "sha256",
    "license",
    "notes",
]


def _cell(value: Any) -> str:
    return "" if value is None else str(value)


def render_csv(observations: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for row in observations:
        institution = row["institution"]
        source = row["source"]
        writer.writerow(
            [
                row["id"],
                row["edition"],
                row["indicator"],
                institution["id"],
                institution["name"],
                institution["kind"],
                row["side"],
                _cell(row["value"]),
                row["value_as_published"],
                row["unit"],
                row["as_of_date"],
                row["date_basis"],
                _cell(row.get("operation_date")),
                row["status"],
                _cell(row.get("retraction_reason")),
                source["name"],
                source["publisher_id"],
                _cell(source.get("upstream_id")),
                source["url"],
                _cell(source.get("locator")),
                source["accessed_at"],
                _cell(source.get("archive_url")),
                _cell(source.get("sha256")),
                source["license"],
                _cell(row.get("notes")),
            ]
        )
    return buffer.getvalue()


def render_empty_latest() -> str:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "edition": None,
        "notice": NOTICE,
        "freshness_max_days": FRESHNESS_MAX_DAYS,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_latest(document: dict[str, Any]) -> str:
    statuses = {edition["status"] for edition in document["editions"]}
    if "published" in statuses or "retracted" in statuses:
        return render_published_latest(document)
    return render_empty_latest()


def main(argv: list[str]) -> int:
    check = "--check" in argv
    if not OBSERVATIONS_PATH.exists():
        print(f"ERROR no existe {OBSERVATIONS_PATH}", file=sys.stderr)
        return 1
    errors = collect_errors()
    if errors:
        print("ERROR observations.json inválido; ejecuta scripts/validate_fx.py", file=sys.stderr)
        return 1

    document = load_json(OBSERVATIONS_PATH)
    latest = render_latest(document)
    outputs = {CSV_PATH: render_csv(document["observations"]), LATEST_PATH: latest}

    stale = [
        path
        for path, text in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != text
    ]
    if check:
        if stale:
            names = ", ".join(path.name for path in stale)
            print(f"ERROR derivados desactualizados: {names}. Ejecuta build_fx.py", file=sys.stderr)
            return 1
        print("OK derivados FX al día")
        return 0

    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK escritos {CSV_PATH.name} y {LATEST_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
