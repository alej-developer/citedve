"""Espejo Pydantic v2 de `packages/schema/signals.schema.json`.

Cualquier cambio en el contrato debe reflejarse en el JSON Schema, en
`packages/schema/src/index.ts` y aquí. `tests/test_schema_parity.py` vigila la paridad.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1.0"

Domain = Literal["fx", "inflation", "energy", "sanctions", "fintech", "ecommerce", "digital_infra"]
ClaimType = Literal["fact", "range", "hypothesis"]
Confidence = Literal["low", "medium", "high"]

_HTTP_URL = r"^https?://[^\s]+$"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(_Strict):
    name: str = Field(min_length=2, max_length=120)
    url: str = Field(pattern=_HTTP_URL)
    captured_at: date
    published_at: date | None = None
    archive_url: str | None = Field(default=None, pattern=_HTTP_URL)


class ValueRange(_Strict):
    min: float
    max: float


class Signal(_Strict):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{2,80}$")
    edition: date
    domain: Domain
    indicator: str = Field(pattern=r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")
    claim_type: ClaimType
    title: str = Field(min_length=3, max_length=160)
    statement: str = Field(min_length=10, max_length=1200)
    value: float | None = None
    unit: str | None = Field(default=None, max_length=40)
    range: ValueRange | None = None
    observed_at: date
    sources: list[Source] = Field(min_length=1)
    confidence: Confidence | None = None
    assumptions: list[str] | None = Field(default=None, min_length=1)
    falsifiers: list[str] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _check_claim_rules(self) -> Signal:
        if self.claim_type == "range":
            if self.range is None or self.unit is None:
                raise ValueError("claim_type=range exige 'range' y 'unit'")
            if len(self.sources) < 2:
                raise ValueError("claim_type=range exige al menos 2 fuentes")
        if self.claim_type == "hypothesis" and (
            self.confidence is None or self.assumptions is None or self.falsifiers is None
        ):
            raise ValueError(
                "claim_type=hypothesis exige 'confidence', 'assumptions', 'falsifiers'"
            )
        return self


class SignalsDocument(_Strict):
    schema_version: Literal["0.1.0"]
    signals: list[Signal]


class LatestDocument(_Strict):
    schema_version: Literal["0.1.0"]
    edition: date | None
    signals: list[Signal]
