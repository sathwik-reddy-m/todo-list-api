from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "todo-list-api"


def test_create_todo():
    response = client.post(
        "/todos",
        json= {
            "title" : "Write tests",
            "completed" : False
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] == False
    assert "id" in data

def test_get_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_todo():
    create = client.post(
        "/todos",
        json= {"title":"Single todo", "completed": False}
    )
    todo_id = create.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

def test_update_todo():
    create = client.post(
        "/todos",
        json = {"title": "Old title", "completed": False}
    )
    todo_id = create.json()["id"]

    response= client.put(
        f"/todos/{todo_id}",
        json = {"title": "New title", "completed": True}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["completed"] == True


def test_delete_todo():
    create = client.post(
        "/todos",
        json={"title": "To delete","completed": False}
    )
    todo_id = create.json()["id"]

    response= client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    get_deleted = client.get(f"/todos/{todo_id}")
    assert get_deleted.status_code == 404