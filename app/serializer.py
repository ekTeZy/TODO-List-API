from app import db
from .models import Task

class TaskSerializer:
    """
    Сериализатор для модели Task.
    Этот класс предоставляет метод для сериализации объектов Task в словарь.
    """

    @staticmethod
    def serialize(task):
        """
        Сериализует объект Task в словарь.
        Args: task (Task): Объект Task, который нужно сериализовать.
        Returns: dict: Словарь, представляющий сериализованный объект Task.
        """
        serialized_task = {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }

        return serialized_task