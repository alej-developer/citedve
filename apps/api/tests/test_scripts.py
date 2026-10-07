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


def _write(tmp_path: Path, doc: dict[str, Any], with_edition: bool = True) -> tuple[Path, Path]:
    signals = tmp_path / "signals.json"
    signals.write_text(json.dumps(doc), encoding="utf-8")
    content = tmp_path / "radar"
    content.mkdir()
    if with_edition:
        (content / "2000-01-03.md").write_text("# edición sintética", encoding="utf-8")
    return signals, content


def test_valid_fixture_passes(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    signals, content = _write(tmp_path, fixture_doc)
    assert validate_signals.collect_errors(signals, SCHEMA, content) == []


def test_missing_edition_file_is_reported(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    signals, content = _write(tmp_path, fixture_doc, with_edition=False)
    errors = validate_signals.collect_errors(signals, SCHEMA, content)
    assert any("content/radar/2000-01-03.md" in e for e in errors)


def test_duplicate_id_is_reported(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    fixture_doc["signals"].append(dict(fixture_doc["signals"][0]))
    signals, content = _write(tmp_path, fixture_doc)
    assert any("duplicado" in e for e in validate_signals.collect_errors(signals, SCHEMA, content))


def test_schema_violation_is_reported(tmp_path: Path, fixture_doc: dict[str, Any]) -> None:
    fixture_doc["signals"][0]["sources"] = []
    signals, content = _write(tmp_path, fixture_doc)
    assert any(
        e.startswith("schema:") for e in validate_signals.collect_errors(signals, SCHEMA, content)
    )


def test_csv_and_latest_render(fixture_doc: dict[str, Any]) -> None:
    signals = build_data.sorted_signals(fixture_doc)
    rows = build_data.render_csv(signals).splitlines()
    assert rows[0].startswith("id,edition,domain")
    assert len(rows) == 4
    assert "Fixture A | Fixture B" in rows[2] or "Fixture A | Fixture B" in "\n".join(rows)
    latest = json.loads(build_data.render_latest(signals))
    assert latest["edition"] == "2000-01-03"
    assert len(latest["signals"]) == 3


def test_latest_empty() -> None:
    latest = json.loads(build_data.render_latest([]))
    assert latest == {"schema_version": "0.1.0", "edition": None, "signals": []}


def test_repo_derivatives_in_sync() -> None:
    assert build_data.main(["--check"]) == 0
