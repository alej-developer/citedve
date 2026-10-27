"""Reglas de integridad FX y derivados vacíos."""

from __future__ import annotations

import copy
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))

import build_fx  # noqa: E402
import validate_fx  # noqa: E402

FIXTURE = REPO / "packages" / "schema" / "fixtures" / "fx_observations.valid.json"
SCHEMA = REPO / "packages" / "schema" / "fx_observations.schema.json"
TODAY = date(2026, 10, 19)


def _write(tmp_path: Path, doc: dict[str, Any]) -> Path:
    path = tmp_path / "observations.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _doc() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return loaded


def _errors(tmp_path: Path, doc: dict[str, Any]) -> list[str]:
    return validate_fx.collect_errors(_write(tmp_path, doc), SCHEMA, today=TODAY)


def _row(doc: dict[str, Any], institution: str, side: str) -> dict[str, Any]:
    for row in doc["observations"]:
        item: dict[str, Any] = row
        if item["institution"]["id"] == institution and item["side"] == side:
            return item
    raise AssertionError(institution)


def test_synthetic_fixture_and_empty_pass(tmp_path: Path) -> None:
    assert _errors(tmp_path, _doc()) == []
    empty = {"schema_version": "0.1.0", "editions": [], "observations": []}
    assert _errors(tmp_path, empty) == []


def test_same_publisher_and_two_upstreams_pass(tmp_path: Path) -> None:
    doc = _doc()
    publishers = {
        _row(doc, "binance-p2p", "compra")["source"]["publisher_id"],
        _row(doc, "bybit-p2p", "compra")["source"]["publisher_id"],
    }
    assert publishers == {"usdt-com-ve"}
    assert _errors(tmp_path, doc) == []


def test_single_p2p_source_fails(tmp_path: Path) -> None:
    doc = _doc()
    doc["observations"] = [
        row
        for row in doc["observations"]
        if not (row["indicator"] == "p2p_referencia" and row["institution"]["id"] == "bybit-p2p")
    ]
    assert any("upstream_id distintos" in err for err in _errors(tmp_path, doc))


def test_same_upstream_does_not_count_as_two(tmp_path: Path) -> None:
    doc = _doc()
    _row(doc, "bybit-p2p", "compra")["source"]["upstream_id"] = "binance-p2p"
    text = " ".join(_errors(tmp_path, doc))
    assert "upstream_id" in text


def test_sin_dato_rejects_published_p2p(tmp_path: Path) -> None:
    doc = _doc()
    doc["editions"][0]["p2p_status"] = "sin_dato"
    assert any("sin_dato" in err for err in _errors(tmp_path, doc))


def test_root_url_missing_citation_and_vetoes(tmp_path: Path) -> None:
    root = _doc()
    root["observations"][0]["source"]["url"] = "https://www.bcv.org.ve/"
    assert any("raíz" in err for err in _errors(tmp_path, root))

    missing = _doc()
    del missing["observations"][0]["source"]["url"]
    assert any(err.startswith("schema:") for err in _errors(tmp_path, missing))

    bapi = _doc()
    bapi["observations"][0]["source"]["url"] = "https://www.bcv.org.ve/bapi/v1"
    assert any("/bapi/" in err for err in _errors(tmp_path, bapi))

    affiliate = _doc()
    affiliate["observations"][0]["source"]["url"] += "?ref=1"
    assert any("afiliado" in err for err in _errors(tmp_path, affiliate))

    discarded = _doc()
    discarded["observations"][0]["source"]["url"] = "https://monitordedivisavenezuela.com/tasa"
    assert any("descartado" in err or "no permitido" in err for err in _errors(tmp_path, discarded))


def test_dates_friday_and_operation_date(tmp_path: Path) -> None:
    late = _doc()
    late["observations"][0]["as_of_date"] = "2026-10-17"
    late["observations"][0]["operation_date"] = "2026-10-17"
    assert any("posterior al corte" in err for err in _errors(tmp_path, late))

    thursday = _doc()
    thursday["editions"][0]["cutoff_date"] = "2026-10-15"
    assert any("no es viernes" in err for err in _errors(tmp_path, thursday))

    valor = _doc()
    _row(valor, "bcv", "venta")["date_basis"] = "fecha_valor"
    assert any("fecha de operación" in err for err in _errors(tmp_path, valor))

    mismatch = _doc()
    _row(mismatch, "bcv", "venta")["operation_date"] = "2026-10-15"
    assert any("fecha de operación" in err for err in _errors(tmp_path, mismatch))


def test_future_cutoff_fails(tmp_path: Path) -> None:
    doc = _doc()
    future = TODAY
    while future.weekday() != 4 or future <= TODAY:
        future += timedelta(days=1)
    iso = future.isocalendar()
    doc["editions"][0]["cutoff_date"] = future.isoformat()
    doc["editions"][0]["id"] = f"{iso.year}-W{iso.week:02d}"
    assert any("posterior a hoy" in err for err in _errors(tmp_path, doc))


def test_bank_minimum_and_official_count(tmp_path: Path) -> None:
    doc = _doc()
    doc["observations"] = [
        row
        for row in doc["observations"]
        if row["institution"]["id"] not in {"banco-beta", "banco-gamma"}
    ]
    assert any("al menos 3 bancos" in err for err in _errors(tmp_path, doc))

    extra = _doc()
    clone = copy.deepcopy(_row(extra, "bcv", "venta"))
    clone["id"] = "fx-2026-W42-tasa_oficial_bcv-bcv-extra-venta"
    clone["institution"]["id"] = "bcv-extra"
    extra["observations"].append(clone)
    text = " ".join(_errors(tmp_path, extra))
    assert "tasa oficial" in text or "schema:" in text


def test_compra_mayor_que_venta_exige_nota(tmp_path: Path) -> None:
    doc = _doc()
    compra = _row(doc, "banco-alfa", "compra")
    compra["value"] = 200
    compra["value_as_published"] = "200,00"
    compra.pop("notes")
    assert any("compra > venta" in err for err in _errors(tmp_path, doc))

    compra["notes"] = "Así lo publica la fuente. Dato sintético."
    assert _errors(tmp_path, doc) == []


def test_transcription_mismatch(tmp_path: Path) -> None:
    doc = _doc()
    doc["observations"][0]["value"] = 101
    assert any("value_as_published" in err for err in _errors(tmp_path, doc))


def test_duplicate_id_and_unknown_edition(tmp_path: Path) -> None:
    dup = _doc()
    dup["observations"].append(copy.deepcopy(dup["observations"][0]))
    assert any("duplicado" in err for err in _errors(tmp_path, dup))

    missing = _doc()
    row = missing["observations"][0]
    row["edition"] = "2026-W41"
    row["id"] = row["id"].replace("2026-W42", "2026-W41")
    assert any("inexistente" in err for err in _errors(tmp_path, missing))


def test_empty_derivatives_have_no_figures() -> None:
    source = (REPO / "scripts" / "build_fx.py").read_text(encoding="utf-8")
    assert "radar_api" not in source
    latest = json.loads(build_fx.render_empty_latest())
    assert latest == {
        "schema_version": "0.1.0",
        "edition": None,
        "notice": "Foto semanal, no cotización en vivo. Información, no asesoramiento.",
        "freshness_max_days": 8,
    }
    csv_text = build_fx.render_csv([])
    assert csv_text.startswith("id,edition,indicator,")
    assert csv_text.count("\n") == 1


def test_published_edition_is_not_rendered_yet() -> None:
    with pytest.raises(build_fx.PublishedEditionPending):
        build_fx.render_latest(_doc())


def test_committed_fx_data_is_empty() -> None:
    path = REPO / "data" / "fx" / "observations.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["editions"] == []
    assert doc["observations"] == []
    assert validate_fx.collect_errors(path, SCHEMA, today=TODAY) == []
