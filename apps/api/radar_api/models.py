"""Espejo Pydantic v2 de `packages/schema/signals.schema.json`."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal, TypeVar, Generic

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1.0"

Category = Literal["fx", "inflation", "energy", "sanctions", "fintech", "ecommerce", "digital_infra", "politics_risk", "other"]
Direction = Literal["up", "down", "flat", "mixed", "n/a"]
Confidence = Literal["low", "medium", "high"]
Status = Literal["published", "draft", "retracted"]

_HTTP_URL = r"^https?://[^\s]+$"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(_Strict):
    name: str = Field(min_length=2, max_length=120)
    url: str = Field(pattern=_HTTP_URL)
    accessed_at: date


class Signal(_Strict):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "id": "bcv-official-rate-jan2024",
                "title": "Tasa oficial del BCV alcanza 36,00 Bs/USD a inicios de 2024",
                "category": "fx",
                "summary": "El Banco Central de Venezuela reporta una tasa oficial promedio de 36,00 Bs/USD en la primera jornada del año.",
                "value_numeric": 36.00,
                "value_text": None,
                "unit": "Bs/USD",
                "as_of_date": "2024-01-02",
                "captured_at": "2024-01-02T16:00:00Z",
                "direction": "flat",
                "confidence": "high",
                "sources": [
                    {
                        "name": "Banco Central de Venezuela",
                        "url": "https://www.bcv.org.ve",
                        "accessed_at": "2024-01-02"
                    }
                ],
                "tags": ["bcv", "exchange_rate"],
                "region": "VE",
                "notes": None,
                "status": "published"
            }
        }
    )

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{2,80}$")
    title: str = Field(min_length=3, max_length=160)
    category: Category
    summary: str = Field(max_length=280)
    value_numeric: float | None = None
    value_text: str | None = None
    unit: str | None = Field(default=None, max_length=40)
    as_of_date: date
    captured_at: datetime
    direction: Direction
    confidence: Confidence
    sources: list[Source] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    region: str = "VE"
    notes: str | None = None
    status: Status

    @model_validator(mode="after")
    def _check_rules(self) -> Signal:
        if self.status == "published":
            if not self.sources:
                raise ValueError("Toda señal published exige >=1 source con URL.")
        return self


class SignalsDocument(_Strict):
    schema_version: Literal["0.1.0"]
    signals: list[Signal]


class LatestDocument(_Strict):
    schema_version: Literal["0.1.0"]
    signals: list[Signal]


T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
