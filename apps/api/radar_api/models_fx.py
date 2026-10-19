"""Espejo Pydantic v2 de `packages/schema/fx_observations.schema.json`.

No modifica el contrato de señales.
"""

from __future__ import annotations

import math
import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

FX_SCHEMA_VERSION = "0.1.0"

FxIndicator = Literal["tasa_oficial_bcv", "tasa_informativa_banco", "p2p_referencia"]
FxInstitutionKind = Literal["banco_central", "banco", "agregado_fuente", "mercado_p2p"]
FxSide = Literal["compra", "venta", "referencia"]
FxUnit = Literal["VES/USD", "VES/USDT"]
FxDateBasis = Literal["fecha_valor", "fecha_operacion", "fecha_indicador", "captura_archivada"]
FxEditionStatus = Literal["draft", "published", "retracted"]
FxP2pStatus = Literal["publicado", "sin_dato"]
FxObservationStatus = Literal["published", "retracted"]

_HTTPS = r"^https://[^\s]+$"
_SLUG = r"^[a-z0-9-]+$"
_XLS = re.compile(r"\.xls$")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class FxEdition(_Strict):
    id: str = Field(pattern=r"^\d{4}-W\d{2}$")
    cutoff_date: date
    status: FxEditionStatus
    p2p_status: FxP2pStatus
    retraction_reason: str | None = Field(default=None, min_length=1)
    notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _retracted_needs_reason(self) -> FxEdition:
        if self.status == "retracted" and not self.retraction_reason:
            raise ValueError("Una edición retracted exige retraction_reason.")
        return self


class FxInstitution(_Strict):
    id: str = Field(min_length=1, pattern=_SLUG)
    name: str = Field(min_length=1, max_length=160)
    kind: FxInstitutionKind


class FxSource(_Strict):
    name: str = Field(min_length=2, max_length=160)
    publisher_id: str = Field(min_length=1, pattern=_SLUG)
    upstream_id: str | None = Field(default=None, min_length=1, pattern=_SLUG)
    url: str = Field(pattern=_HTTPS)
    locator: str | None = Field(default=None, min_length=1)
    accessed_at: datetime
    archive_url: str | None = Field(default=None, pattern=_HTTPS)
    sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    license: str = Field(min_length=1, max_length=200)

    @field_validator("accessed_at")
    @classmethod
    def _aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("accessed_at exige zona horaria.")
        return value


class FxObservation(_Strict):
    id: str = Field(
        pattern=(
            r"^fx-\d{4}-W\d{2}-(tasa_oficial_bcv|tasa_informativa_banco|p2p_referencia)"
            r"-[a-z0-9-]+-(compra|venta|referencia)$"
        )
    )
    edition: str = Field(pattern=r"^\d{4}-W\d{2}$")
    indicator: FxIndicator
    institution: FxInstitution
    side: FxSide
    value: float = Field(gt=0)
    value_as_published: str = Field(min_length=1, max_length=40)
    unit: FxUnit
    as_of_date: date
    date_basis: FxDateBasis
    operation_date: date | None = None
    status: FxObservationStatus
    retraction_reason: str | None = Field(default=None, min_length=1)
    source: FxSource
    notes: str | None = Field(default=None, min_length=1)

    @field_validator("value")
    @classmethod
    def _finite(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("value debe ser finito.")
        return value

    @model_validator(mode="after")
    def _conditional(self) -> FxObservation:
        if self.status == "retracted" and not self.retraction_reason:
            raise ValueError("Una observación retracted exige retraction_reason.")
        if self.indicator == "tasa_oficial_bcv" and self.operation_date is None:
            raise ValueError("tasa_oficial_bcv exige operation_date.")
        if self.indicator == "p2p_referencia" and not self.source.archive_url:
            raise ValueError("p2p_referencia exige source.archive_url.")
        if _XLS.search(self.source.url) and (not self.source.sha256 or not self.source.locator):
            raise ValueError("Un libro .xls exige sha256 y locator.")
        return self


class FxObservationsDocument(_Strict):
    schema_version: Literal["0.1.0"]
    editions: list[FxEdition]
    observations: list[FxObservation]
