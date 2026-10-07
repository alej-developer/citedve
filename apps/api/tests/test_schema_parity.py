"""JSON Schema y espejo Pydantic deben aceptar y rechazar lo mismo."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError
from radar_api.models import SignalsDocument

REPO = Path(__file__).resolve().parents[3]
SCHEMA = json.loads((REPO / "packages" / "schema" / "signals.schema.json").read_text("utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

Mutation = Callable[[dict[str, Any]], None]


def _sig(doc: dict[str, Any], claim: str) -> dict[str, Any]:
    for s in doc["signals"]:
        if s["claim_type"] == claim:
            found: dict[str, Any] = s
            return found
    raise AssertionError(claim)


def _no_sources(d: dict[str, Any]) -> None:
    _sig(d, "fact")["sources"] = []


def _source_missing_captured(d: dict[str, Any]) -> None:
    del _sig(d, "fact")["sources"][0]["captured_at"]


def _bad_url(d: dict[str, Any]) -> None:
    _sig(d, "fact")["sources"][0]["url"] = "no-es-url"


def _range_one_source(d: dict[str, Any]) -> None:
    _sig(d, "range")["sources"] = _sig(d, "range")["sources"][:1]


def _range_without_range(d: dict[str, Any]) -> None:
    del _sig(d, "range")["range"]


def _hypothesis_without_falsifiers(d: dict[str, Any]) -> None:
    del _sig(d, "hypothesis")["falsifiers"]


def _unknown_domain(d: dict[str, Any]) -> None:
    _sig(d, "fact")["domain"] = "politica"


def _extra_field(d: dict[str, Any]) -> None:
    _sig(d, "fact")["inventado"] = True


def _bad_date(d: dict[str, Any]) -> None:
    _sig(d, "fact")["observed_at"] = "03/01/2000"


INVALID: list[Mutation] = [
    _no_sources,
    _source_missing_captured,
    _bad_url,
    _range_one_source,
    _range_without_range,
    _hypothesis_without_falsifiers,
    _unknown_domain,
    _extra_field,
    _bad_date,
]


def _pydantic_ok(doc: dict[str, Any]) -> bool:
    try:
        SignalsDocument.model_validate(doc)
    except ValidationError:
        return False
    return True


def test_valid_fixture_accepted_by_both(fixture_doc: dict[str, Any]) -> None:
    assert not list(VALIDATOR.iter_errors(fixture_doc))
    assert _pydantic_ok(fixture_doc)


def test_empty_document_accepted_by_both() -> None:
    doc = {"schema_version": "0.1.0", "signals": []}
    assert VALIDATOR.is_valid(doc)
    assert _pydantic_ok(doc)


@pytest.mark.parametrize("mutate", INVALID, ids=lambda f: f.__name__.lstrip("_"))
def test_invalid_rejected_by_both(fixture_doc: dict[str, Any], mutate: Mutation) -> None:
    doc = copy.deepcopy(fixture_doc)
    mutate(doc)
    assert not VALIDATOR.is_valid(doc), "JSON Schema debería rechazarlo"
    assert not _pydantic_ok(doc), "Pydantic debería rechazarlo"
