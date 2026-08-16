from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_welcome_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome"}


def test_health_check_route():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
