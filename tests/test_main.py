from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRoot:
    def test_root_returns_message(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "TestPilot API is running"}


class TestHealth:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
