import requests
from app.config import Config

"""
Модуль для выполнения POST-запроса к API.

Этот модуль использует библиотеку requests для отправки POST-запроса к API,
определенному по URL "http://localhost:5000/tasks/5". Заголовки запроса включают
Content-type: application/json. Данные, отправляемые в запросе, включают заголовок
задачи и статус задачи. В комментариях указано место для добавления авторизации.

Пример использования:
    response = requests.post(url=url, json=data, headers=headers)
    data = response.json()
    print(data)
    print(response.status_code)
Должно вернуть:
    {'msg': 'Task created successfully', 'properties': {'status': 'todo', 'title': 'Todo Task'}}
    201
"""

headers = {
    "Content-type": "application/json"
}
data = {
    "title": "Todo Task",
    "status": "todo",
    "Authorization": f"{Config.AUTHORIZATION_PASS}"
}

url = "http://localhost:5000/tasks/"


response = requests.post(url=url, json=data, headers=headers)
data = response.json()
print(data)
print(response.status_code)