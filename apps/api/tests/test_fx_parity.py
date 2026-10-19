"""JSON Schema FX y espejo Pydantic deben aceptar y rechazar lo mismo."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError
from radar_api.models_fx import FxObservationsDocument

REPO = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO / "packages" / "schema" / "fx_observations.schema.json").read_text("utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)
FIXTURE = REPO / "packages" / "schema" / "fixtures" / "fx_observations.valid.json"

Mutation = Callable[[dict[str, Any]], None]


def _load() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return loaded


def _find(doc: dict[str, Any], indicator: str, institution: str, side: str) -> dict[str, Any]:
    for row in doc["observations"]:
        item: dict[str, Any] = row
        if (
            item["indicator"] == indicator
            and item["institution"]["id"] == institution
            and item["side"] == side
        ):
            return item
    raise AssertionError(f"no está la fila {indicator}/{institution}/{side}")


def _extra_field(doc: dict[str, Any]) -> None:
    doc["observations"][0]["inventado"] = True


def _bad_version(doc: dict[str, Any]) -> None:
    doc["schema_version"] = "9.9.9"


def _edition_retracted_without_reason(doc: dict[str, Any]) -> None:
    doc["editions"][0]["status"] = "retracted"
    doc["editions"][0].pop("retraction_reason", None)


def _observation_retracted_without_reason(doc: dict[str, Any]) -> None:
    row = doc["observations"][0]
    row["status"] = "retracted"
    row.pop("retraction_reason", None)


def _official_without_operation_date(doc: dict[str, Any]) -> None:
    _find(doc, "tasa_oficial_bcv", "bcv", "venta").pop("operation_date")


def _p2p_without_archive(doc: dict[str, Any]) -> None:
    _find(doc, "p2p_referencia", "binance-p2p", "compra")["source"].pop("archive_url")


def _xls_without_sha256(doc: dict[str, Any]) -> None:
    _find(doc, "tasa_oficial_bcv", "bcv", "venta")["source"].pop("sha256")


def _xls_without_locator(doc: dict[str, Any]) -> None:
    _find(doc, "tasa_oficial_bcv", "bcv", "compra")["source"].pop("locator")


def _zero_value(doc: dict[str, Any]) -> None:
    doc["observations"][0]["value"] = 0


def _negative_value(doc: dict[str, Any]) -> None:
    doc["observations"][0]["value"] = -1


def _http_url(doc: dict[str, Any]) -> None:
    doc["observations"][0]["source"]["url"] = "http://www.bcv.org.ve/estadisticas/tipo-cambio"


def _bad_sha256(doc: dict[str, Any]) -> None:
    _find(doc, "tasa_oficial_bcv", "bcv", "venta")["source"]["sha256"] = "abc"


def _unknown_indicator(doc: dict[str, Any]) -> None:
    doc["observations"][0]["indicator"] = "remesas"


def _missing_license(doc: dict[str, Any]) -> None:
    doc["observations"][0]["source"].pop("license")


def _bad_edition_id(doc: dict[str, Any]) -> None:
    doc["editions"][0]["id"] = "2026-10-16"


def _naive_accessed_at(doc: dict[str, Any]) -> None:
    doc["observations"][0]["source"]["accessed_at"] = "2026-10-16T18:00:00"


INVALID: list[Mutation] = [
    _extra_field,
    _bad_version,
    _edition_retracted_without_reason,
    _observation_retracted_without_reason,
    _official_without_operation_date,
    _p2p_without_archive,
    _xls_without_sha256,
    _xls_without_locator,
    _zero_value,
    _negative_value,
    _http_url,
    _bad_sha256,
    _unknown_indicator,
    _missing_license,
    _bad_edition_id,
    _naive_accessed_at,
]


def _pydantic_ok(doc: dict[str, Any]) -> bool:
    try:
        FxObservationsDocument.model_validate(doc)
    except ValidationError:
        return False
    return True


def test_valid_fixture_is_labelled_synthetic() -> None:
    notes = _load()["editions"][0]["notes"]
    assert "sintética" in notes
    assert "no se publica" in notes


def test_valid_fixture_accepted_by_both() -> None:
    doc = _load()
    assert not list(VALIDATOR.iter_errors(doc))
    assert _pydantic_ok(doc)


def test_empty_document_accepted_by_both() -> None:
    doc = {"schema_version": "0.1.0", "editions": [], "observations": []}
    assert VALIDATOR.is_valid(doc)
    assert _pydantic_ok(doc)


def test_compra_mayor_que_venta_sigue_en_el_esquema() -> None:
    doc = _load()
    compra = _find(doc, "tasa_informativa_banco", "banco-alfa", "compra")
    venta = _find(doc, "tasa_informativa_banco", "banco-alfa", "venta")
    compra["value"] = 200
    compra["value_as_published"] = "200,00"
    venta["value"] = 100
    venta["value_as_published"] = "100,00"
    compra.pop("notes", None)
    assert VALIDATOR.is_valid(doc)
    assert _pydantic_ok(doc)


@pytest.mark.parametrize("mutate", INVALID, ids=lambda fn: fn.__name__.lstrip("_"))
def test_invalid_rejected_by_both(mutate: Mutation) -> None:
    doc = copy.deepcopy(_load())
    mutate(doc)
    schema_errors = list(VALIDATOR.iter_errors(doc))
    assert schema_errors, "JSON Schema debería rechazarlo"
    assert not _pydantic_ok(doc), "Pydantic debería rechazarlo"
