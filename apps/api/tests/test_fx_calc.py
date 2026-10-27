"""Cálculos FX puros y el derivado de una edición sintética."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from radar_api.fx import bank_dispersion, gap_label, median, p2p_bounds, render_published_latest

REPO = Path(__file__).resolve().parents[3]
CASES = REPO / "packages" / "schema" / "fixtures" / "fx_gap_cases.json"
FIXTURE = REPO / "packages" / "schema" / "fixtures" / "fx_observations.valid.json"


def _doc() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return loaded


def test_gap_labels_match_the_shared_fixture() -> None:
    cases: list[dict[str, Any]] = json.loads(CASES.read_text(encoding="utf-8"))
    for case in cases:
        assert gap_label(case["official"], case["parallel"]) == case["label"]


def test_median_odd_even_and_short_inputs() -> None:
    assert median([3, 1, 2]) == 2
    assert median([150, 160]) == 155
    assert median([10]) is None
    assert median([10, 0]) is None
    assert median([float("nan"), 10]) is None


def test_bounds_need_two_positive_values() -> None:
    assert p2p_bounds([160, 150]) == (150, 160)
    assert p2p_bounds([10]) is None
    assert p2p_bounds([10, -1]) is None
    assert p2p_bounds([10, float("inf")]) is None


def test_dispersion_skips_aggregates_and_names_nobody() -> None:
    rows = [
        _bank("alfa", "banco", "compra", 130),
        _bank("beta", "banco", "compra", 110),
        _bank("otras", "agregado_fuente", "compra", 1),
        _bank("gamma", "banco", "venta", 140),
    ]
    result = bank_dispersion(rows, "compra")
    assert result == {"min": 110, "max": 130, "amplitud": 20, "n": 2}
    assert result is not None
    assert "alfa" not in json.dumps(result)


def test_synthetic_edition_orders_banks_and_labels_gaps() -> None:
    latest = json.loads(render_published_latest(_doc()))
    names = [row["institution"]["name"] for row in latest["banks"]]
    assert names == [
        "Banco Alfa (sintético)",
        "Banco Beta (sintético)",
        "Banco Gamma (sintético)",
        "Otras Instituciones",
    ]
    assert latest["dispersion"]["compra"] == {"min": 110.0, "max": 130.0, "amplitud": 20.0, "n": 3}
    assert latest["p2p"]["side"] == "compra"
    assert latest["p2p"]["min"] == 150
    assert latest["p2p"]["max"] == 160
    assert latest["p2p"]["mediana"] == 155
    assert [gap["text"] for gap in latest["gaps"]] == ["48.5%", "58.4%", "53.5%"]
    assert latest["official"]["venta"]["value"] == 101
    dumped = json.dumps(latest)
    assert "mejor" not in dumped
    assert "sintética" in latest["edition"]["notes"]


def test_retracted_edition_hides_values() -> None:
    doc = _doc()
    doc["editions"][0]["status"] = "retracted"
    doc["editions"][0]["retraction_reason"] = "Ejemplo sintético retirado"
    latest = json.loads(render_published_latest(doc))
    assert latest["edition"] is None
    assert latest["retracted_banner"] == "La edición 2026-W42 se retiró: Ejemplo sintético retirado"
    assert "official" not in latest
    assert "100" not in json.dumps(latest)


def test_retracted_row_hides_its_value() -> None:
    doc = _doc()
    for row in doc["observations"]:
        if row["institution"]["id"] == "banco-alfa" and row["side"] == "compra":
            row["status"] = "retracted"
            row["retraction_reason"] = "Fila sintética retirada"
    latest = json.loads(render_published_latest(doc))
    alfa = latest["banks"][0]["compra"]
    assert alfa["value"] is None
    assert alfa["value_as_published"] is None
    assert alfa["retraction_reason"] == "Fila sintética retirada"
    assert latest["dispersion"]["compra"]["n"] == 2


def _bank(name: str, kind: str, side: str, value: float) -> dict[str, Any]:
    return {
        "indicator": "tasa_informativa_banco",
        "side": side,
        "status": "published",
        "value": value,
        "institution": {"id": name, "name": name, "kind": kind},
    }
