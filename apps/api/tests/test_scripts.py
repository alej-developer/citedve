from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))

import build_data  # noqa: E402
import validate_signals  # noqa: E402

SCHEMA = REPO / "packages" / "schema" / "signals.schema.json"


def _write(tmp_path: Path, doc: dict[str, Any]) -> Path:
    signals = tmp_path / "signals.json"
    signals.write_text(json.dumps(doc), encoding="utf-8")
    return signals


def test_valid_fixture_passes(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    signals = _write(tmp_path, fixture_doc)
    assert validate_signals.collect_errors(signals, SCHEMA) == []


def test_duplicate_id_is_reported(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    fixture_doc["signals"].append(dict(fixture_doc["signals"][0]))
    signals = _write(tmp_path, fixture_doc)
    assert any("duplicado" in e for e in validate_signals.collect_errors(signals, SCHEMA))


def test_schema_violation_is_reported(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    fixture_doc["signals"][0]["sources"] = []
    signals = _write(tmp_path, fixture_doc)
    assert any(e.startswith("schema:") for e in validate_signals.collect_errors(signals, SCHEMA))


def test_csv_and_latest_render(fixture_doc: dict[str, Any]) -> None:
    signals = build_data.sorted_signals(fixture_doc)
    rows = build_data.render_csv(signals).splitlines()
    assert rows[0].startswith("id,title,category")
    assert len(rows) == 2
    latest = json.loads(build_data.render_latest(signals))
    assert len(latest["signals"]) == 1
    assert latest["signals"][0]["id"] == "bcv-official-rate-jan2024"


def test_latest_empty() -> None:
    latest = json.loads(build_data.render_latest([]))
    assert latest == {"schema_version": "0.1.0", "signals": []}


def test_repo_derivatives_in_sync() -> None:
    assert build_data.main(["--check"]) == 0
