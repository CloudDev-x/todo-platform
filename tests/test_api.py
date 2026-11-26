import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_index_is_served(client):
    assert client.get("/").status_code == 200


def test_create_and_list(client):
    res = client.post("/api/todos", json={"text": "write tests"})
    assert res.status_code == 201
    assert res.json() == {"id": 1, "text": "write tests", "done": False}
    assert client.get("/api/todos").json() == [
        {"id": 1, "text": "write tests", "done": False}
    ]


def test_create_empty_returns_400(client):
    res = client.post("/api/todos", json={"text": "   "})
    assert res.status_code == 400
    assert "error" in res.json()


def test_toggle(client):
    client.post("/api/todos", json={"text": "walk"})
    res = client.patch("/api/todos/1")
    assert res.status_code == 200
    assert res.json()["done"] is True


def test_toggle_missing_returns_404(client):
    assert client.patch("/api/todos/999").status_code == 404


def test_delete(client):
    client.post("/api/todos", json={"text": "temp"})
    assert client.delete("/api/todos/1").status_code == 204
    assert client.get("/api/todos").json() == []


def test_delete_missing_returns_404(client):
    assert client.delete("/api/todos/999").status_code == 404
