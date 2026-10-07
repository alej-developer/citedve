from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_and_filter(async_client: AsyncClient) -> None:
    resp = await async_client.get("/v1/signals")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert data["next_cursor"] is None

    # Filtrar por category
    resp = await async_client.get("/v1/signals", params={"category": "fx"})
    assert [s["id"] for s in resp.json()["items"]] == ["bcv-official-rate-jan2024"]

    resp = await async_client.get("/v1/signals", params={"category": "energy"})
    assert len(resp.json()["items"]) == 0


@pytest.mark.asyncio
async def test_invalid_filter_is_rejected(async_client: AsyncClient) -> None:
    resp = await async_client.get("/v1/signals", params={"category": "otro"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_latest(async_client: AsyncClient) -> None:
    resp = await async_client.get("/v1/radar/latest")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["signals"]) == 1
    assert body["signals"][0]["id"] == "bcv-official-rate-jan2024"


@pytest.mark.asyncio
async def test_get_signal_and_404(async_client: AsyncClient) -> None:
    resp = await async_client.get("/v1/signals/bcv-official-rate-jan2024")
    assert resp.status_code == 200
    assert resp.json()["id"] == "bcv-official-rate-jan2024"

    resp = await async_client.get("/v1/signals/no-existe")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_meta_routes(async_client: AsyncClient) -> None:
    resp = await async_client.get("/v1/meta/categories")
    assert resp.status_code == 200
    assert "fx" in resp.json()

    resp = await async_client.get("/v1/meta/sources")
    assert resp.status_code == 200
    assert "Banco Central de Venezuela" in resp.json()
