from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from radar_api.config import settings
from radar_api.main import app

REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "packages" / "schema" / "fixtures" / "valid.json"


@pytest.fixture
def fixture_doc() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return data


@pytest_asyncio.fixture
async def async_client(
    tmp_path: Path, fixture_doc: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> AsyncGenerator[AsyncClient, None]:
    """Cliente asíncrono apuntando a un directorio de datos temporal con fixtures sintéticos."""
    (tmp_path / "signals.json").write_text(json.dumps(fixture_doc), encoding="utf-8")
    monkeypatch.setenv("RADAR_DATA_DIR", str(tmp_path))
    # We must reset the config value explicitly if it was already loaded
    settings.data_dir = str(tmp_path)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
