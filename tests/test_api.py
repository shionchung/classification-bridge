"""HTTP-level checks for the FastAPI classification service."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api import app

STEEL_UNICLASS_PR = "Pr_20_93_74_16"


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_redirects_to_docs(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/docs"


def test_map_uniclass_known(client):
    response = client.get(f"/map/uniclass/{STEEL_UNICLASS_PR}")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "found"
    assert body["classification"]["uniclass"]["pr"] == STEEL_UNICLASS_PR
    assert body["classification"]["nlsfb"]["material"] == "Q5"
    assert body["review_status"] == "verified"


def test_map_uniclass_unknown_returns_404(client):
    response = client.get("/map/uniclass/Pr_99_99_99_99")
    assert response.status_code == 404
    assert response.json()["detail"]["status"] == "not_found"


def test_search_steel(client):
    response = client.get("/search/steel")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    pr_codes = [
        r["classification"]["uniclass"]["pr"] for r in body["results"]
    ]
    assert STEEL_UNICLASS_PR in pr_codes


def test_materials_lists_mappings(client):
    response = client.get("/materials")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 20


def test_materials_filter_verified(client):
    response = client.get("/materials", params={"review_status": "verified"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 5
    assert all(m["review_status"] == "verified" for m in body["materials"])
