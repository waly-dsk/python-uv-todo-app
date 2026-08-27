from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_welcome_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health_check_route():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_todos():
    response = client.get("/get_todos")
    assert response.status_code == 200
    # On vérifie juste que la réponse contient bien la clé "todos"
    assert "todos" in response.json()
