from .config import Config

class TaskValidator:
    """
    Класс валидатора для данных задачи.
    """

    @staticmethod
    def validate_post_data(data):
        """
        Валидирует данные для создания новой задачи.
        Args: data (dict): Данные для валидации.
        Raises: Exception: Если данные неверны.
        Returns: bool: True, если данные верны.
        """
        if not data or not isinstance(data, dict):
            raise Exception("Invalid data: JSON object expected.")

        if "title" not in data or not isinstance(data["title"], str) or not data["title"].strip():
            raise Exception("Invalid 'title' field: must be a non-empty string.")

        status = data.get("status", "todo")

        if status not in ["todo", "done"]:
            raise Exception(f"Invalid 'status' field: {status}. Must be 'todo' or 'done'.")

        return True

    @staticmethod
    def validate_patch_data(data):
        """
        Валидирует данные для обновления существующей задачи.
        Args: data (dict): Данные для валидации.
        Raises: Exception: Если данные неверны.
        Returns: bool: True, если данные верны.
        """
        if not data or not isinstance(data, dict):
            raise Exception("Invalid data: JSON object expected.")

        if "status" not in data:
            raise Exception("'status' field is required for update.")

        if data["status"] not in ["todo", "done"]:
            raise Exception(f"Invalid 'status' field: {data['status']}. Must be 'todo' or 'done'.")

        return True
    
    @staticmethod
    def validate_delete_data(data):
        """
        Проверяет авторизацию для удаления данных.
        Args: data (dict): Данные в формате JSON, содержащие ключ "Authorization".
        Returns:bool: True, если авторизация прошла успешно.
        Raises: Exception: Если авторизация не пройдена, выбрасывается исключение с сообщением "Unauthorized. Check password in request."
        """
        if not data["Authorization"] == str(Config.AUTHORIZATION_PASS):
            raise Exception("Unauthorized. Check password in request.")

        return True