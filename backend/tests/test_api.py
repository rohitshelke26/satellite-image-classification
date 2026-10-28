from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert "model_loaded" in response.json()


def test_classes():
    with TestClient(app) as client:
        response = client.get("/api/classes")
        assert response.status_code == 200
        assert len(response.json()) == 10


def test_rejects_text():
    with TestClient(app) as client:
        response = client.post(
            "/api/predict",
            files={"file": ("notes.txt", b"not an image", "text/plain")},
        )
        assert response.status_code == 415
