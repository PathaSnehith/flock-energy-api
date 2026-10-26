
from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_meters_requires_valid_page():
    with TestClient(app) as client:
        response = client.get("/api/meters?page=0")

    assert response.status_code == 422


def test_openapi_available():
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()
