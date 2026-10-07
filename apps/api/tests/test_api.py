from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_and_filter(client: TestClient) -> None:
    assert len(client.get("/v1/signals").json()) == 3
    only_range = client.get("/v1/signals", params={"claim_type": "range"}).json()
    assert [s["id"] for s in only_range] == ["fixture-range-001"]
    assert client.get("/v1/signals", params={"domain": "sanctions"}).json()[0]["claim_type"] == (
        "hypothesis"
    )


def test_invalid_filter_is_rejected(client: TestClient) -> None:
    assert client.get("/v1/signals", params={"domain": "otro"}).status_code == 422


def test_latest(client: TestClient) -> None:
    body = client.get("/v1/signals/latest").json()
    assert body["edition"] == "2000-01-03"
    assert len(body["signals"]) == 3


def test_get_signal_and_404(client: TestClient) -> None:
    assert client.get("/v1/signals/fixture-fact-001").status_code == 200
    assert client.get("/v1/signals/no-existe").status_code == 404
