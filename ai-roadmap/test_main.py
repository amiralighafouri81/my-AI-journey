import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory storage before each test."""
    main.notes.clear()
    main.next_id = 1
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Note API"


def test_create_note():
    response = client.post(
        "/notes",
        json={"title": "Test note", "content": "Test content"},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test note"
    assert data["content"] == "Test content"


def test_get_notes():
    client.post("/notes", json={"title": "A", "content": "B"})
    client.post("/notes", json={"title": "C", "content": "D"})

    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_note():
    client.post("/notes", json={"title": "A", "content": "B"})

    response = client.get("/notes/1")
    assert response.status_code == 200
    assert response.json()["title"] == "A"


def test_get_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404


def test_update_note():
    client.post("/notes", json={"title": "A", "content": "B"})

    response = client.patch("/notes/1", json={"content": "Updated"})
    assert response.status_code == 200
    assert response.json()["content"] == "Updated"
    assert response.json()["title"] == "A"  # unchanged


def test_delete_note():
    client.post("/notes", json={"title": "A", "content": "B"})

    response = client.delete("/notes/1")
    assert response.status_code == 204

    assert client.get("/notes/1").status_code == 404


def test_validation_error():
    response = client.post("/notes", json={"content": "no title"})
    assert response.status_code == 422


def test_error_demo():
    assert client.get("/error-demo/401").status_code == 401
    assert client.get("/error-demo/429").status_code == 429
    assert client.get("/error-demo/200").status_code == 200


def test_simulate_llm(monkeypatch):
    """Mock asyncio.sleep so the test runs instantly."""

    async def fake_sleep(seconds):
        pass

    monkeypatch.setattr(main.asyncio, "sleep", fake_sleep)

    response = client.get("/simulate/llm", params={"prompt": "hello"})
    assert response.status_code == 200
    assert response.json()["response"] == "Mock LLM reply to: hello"
