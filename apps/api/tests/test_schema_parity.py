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


def _sig(doc: dict[str, Any]) -> dict[str, Any]:
    signal: dict[str, Any] = doc["signals"][0]
    return signal


def _no_sources_when_published(d: dict[str, Any]) -> None:
    s = _sig(d)
    s["status"] = "published"
    s["sources"] = []


def _source_missing_accessed_at(d: dict[str, Any]) -> None:
    s = _sig(d)
    s["sources"] = [{"name": "BCV", "url": "https://www.bcv.org.ve"}]


def _bad_url(d: dict[str, Any]) -> None:
    s = _sig(d)
    s["sources"] = [{"name": "BCV", "url": "no-es-url", "accessed_at": "2024-01-01"}]


def _unknown_category(d: dict[str, Any]) -> None:
    _sig(d)["category"] = "politica"


def _extra_field(d: dict[str, Any]) -> None:
    _sig(d)["inventado"] = True


def _bad_date(d: dict[str, Any]) -> None:
    _sig(d)["as_of_date"] = "03/01/2000"


INVALID: list[Mutation] = [
    _no_sources_when_published,
    _source_missing_accessed_at,
    _bad_url,
    _unknown_category,
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
