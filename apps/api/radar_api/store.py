"""Acceso a los datos versionados en Git. Sin base de datos en el MVP (ver docs/ARCHITECTURE.md)."""

from __future__ import annotations

import os
from pathlib import Path

from radar_api.models import LatestDocument, Signal, SignalsDocument

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def data_dir() -> Path:
    return Path(os.environ.get("RADAR_DATA_DIR", str(DEFAULT_DATA_DIR)))


def load_signals(directory: Path | None = None) -> list[Signal]:
    path = (directory or data_dir()) / "signals.json"
    document = SignalsDocument.model_validate_json(path.read_text(encoding="utf-8"))
    return document.signals


def load_latest(directory: Path | None = None) -> LatestDocument:
    path = (directory or data_dir()) / "latest.json"
    return LatestDocument.model_validate_json(path.read_text(encoding="utf-8"))
