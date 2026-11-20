import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_todos.db"
    monkeypatch.setenv("DB_PATH", str(db_file))


def test_read_root_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<!DOCTYPE html>" in response.text or "<html" in response.text
    assert "Todo List" in response.text


def test_create_todo():
    response = client.post("/todos", json={"title": "Buy groceries", "description": "Milk, Eggs, Bread"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, Eggs, Bread"
    assert data["completed"] is False


def test_list_todos():
    client.post("/todos", json={"title": "Task 1"})
    client.post("/todos", json={"title": "Task 2"})
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_todo_success():
    create_resp = client.post("/todos", json={"title": "Read book", "description": "FastAPI chapter"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Read book"


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo_success():
    create_resp = client.post("/todos", json={"title": "Exercise"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True, "description": "30 mins run"})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["description"] == "30 mins run"
    assert data["title"] == "Exercise"


def test_update_todo_not_found():
    response = client.put("/todos/999", json={"title": "Non-existent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo_success():
    create_resp = client.post("/todos", json={"title": "Temporary Task"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_toggle_todo_false_to_true():
    create_resp = client.post("/todos", json={"title": "Toggle test 1", "completed": False})
    todo_id = create_resp.json()["id"]
    response = client.patch(f"/todos/{todo_id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] is True


def test_toggle_todo_true_to_false():
    create_resp = client.post("/todos", json={"title": "Toggle test 2", "completed": True})
    todo_id = create_resp.json()["id"]
    response = client.patch(f"/todos/{todo_id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] is False


def test_toggle_todo_not_found():
    response = client.patch("/todos/999/toggle")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
