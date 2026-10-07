from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from radar_api.main import app

REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "packages" / "schema" / "fixtures" / "valid.json"


@pytest.fixture
def fixture_doc() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return data


@pytest.fixture
def client(
    tmp_path: Path, fixture_doc: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> TestClient:
    """Cliente apuntando a un directorio de datos temporal con fixtures sintéticos."""
    (tmp_path / "signals.json").write_text(json.dumps(fixture_doc), encoding="utf-8")
    latest = {
        "schema_version": "0.1.0",
        "edition": "2000-01-03",
        "signals": fixture_doc["signals"],
    }
    (tmp_path / "latest.json").write_text(json.dumps(latest), encoding="utf-8")
    monkeypatch.setenv("RADAR_DATA_DIR", str(tmp_path))
    return TestClient(app)
