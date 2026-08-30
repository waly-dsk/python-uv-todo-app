from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def create_test_todo():
    response = client.post(
        "/todos",
        json={
            "title": "Todo de test",
            "content": "Test content",
        },
    )

    return response.json()["id"]


def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_create_todo():
    response = client.post(
        "/todos",
        json={
            "title": "Test Todo",
            "content": "Test content",
        },
    )

    assert response.json()["title"] == "Test Todo"
    assert response.status_code == 200


def test_get_todos():
    todo_id = create_test_todo()
    response = client.get("/todos")

    assert response.status_code == 200

    todos = response.json()

    for todo in todos:
        if todo["id"] == todo_id:
            assert todo["title"] == "Todo de test"


def test_get_todo():
    todo_id = create_test_todo()
    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Todo de test"


def test_update_todo():
    todo_id = create_test_todo()
    response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "Test Todo Updated",
            "content": "Test Content Updated",
            "done": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo Updated"


def test_delete_todo():
    todo_id = create_test_todo()
    response = client.delete(
        f"/todos/{todo_id}",
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"
