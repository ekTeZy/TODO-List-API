import pytest
from app.models import Task
from app import create_app
from app import db
import os 

@pytest.fixture
def app():
    """
    Фикстура для создания тестового приложения.

    Возвращает:
        app: Тестовое приложение.
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """
    Фикстура для создания тестового клиента.

    Аргументы:
        app: Тестовое приложение.

    Возвращает:
        client: Тестовый клиент.
    """
    return app.test_client()

def test_post(client, app):
    """
    Тест для проверки POST-запроса на создание задачи.

    Аргументы:
        client: Тестовый клиент.
        app: Тестовое приложение.
    """
    with app.app_context():
        data_OK = {
            "title": "Test Post Good",
            "status": "todo"
        }

        data_BAD = {
            "title": "Test Post Bad",
            "status": 123
        }

        response_201 = client.post("/tasks/", json=data_OK)
        response_400 = client.post("/tasks/", json=data_BAD)

        assert response_201.status_code == 201
        assert response_201.json == {
                "msg": "Task created successfully",
                "properties": {
                    "title": "Test Post Good",
                    "status": "todo"
                }
            }
        assert response_400.status_code == 400
def test_delete(client, app):
    """
    Тестирует удаление задачи.
    Аргументы:
    - client: Клиент для выполнения HTTP-запросов.
    - app: Приложение Flask.
    """
    with app.app_context():
        new_task = Task(title="Test Delete Item", status="todo")
        db.session.add(new_task)
        db.session.commit()

        good_data = {
            "Authorization": f"{os.getenv('AUTHORIZATION_PASS')}"
        }

        bad_data = {
            "Authorization": "123456"
        }

        good_response = client.delete(f"tasks/{new_task.id}", json=good_data)
        bad_response = client.delete(f"tasks/{new_task.id}", json=bad_data)

        assert good_response.json == {
            "msg": f"Task with id {new_task.id} deleted successfuly."
        }
        assert good_response.status_code == 200

        assert bad_response.json == {
            "error": "Unauthorized. Check password in request."
        }
        assert bad_response.status_code == 400

def test_get_item(client, app):
    """
    Тест для проверки GET-запроса на получение задачи.

    Аргументы:
        client: Тестовый клиент.
        app: Тестовое приложение.
    """
    with app.app_context():
        new_task = Task(title="Test Get Item", status="todo")
        db.session.add(new_task)
        db.session.commit()

        task = db.session.get(Task, new_task.id)

        good_response = client.get(f"/tasks/{new_task.id}")
        bad_response = client.get(f"/tasks/{9999999}")

        assert good_response.status_code == 200
        assert good_response.json == {
                "id": task.id,
                "title": task.title,
                "status": task.status
        }

        assert bad_response.status_code == 404

def test_patch(client, app):
    """
    Тест для проверки PATCH-запроса на обновление задачи.

    Аргументы:
        client: Тестовый клиент.
        app: Тестовое приложение.
    """
    with app.app_context():
        new_task = Task(title="Test Patch", status="todo")
        db.session.add(new_task)
        db.session.commit()

        task = db.session.get(Task, new_task.id)

        data = {"status": "done"}
        response = client.patch(f"/tasks/{task.id}", json=data)

        assert response.status_code == 200
        assert response.json == {
            'id': task.id,
            'title': 'Test Patch',
            'status': 'done'
        }