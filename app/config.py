import os

class Config:
    """
    Класс конфигурации приложения.

    Атрибуты:
        AUTHORIZATION_PASS (str): Пароль для авторизации.
        SECRET_KEY (str): Секретный ключ для шифрования.
        SQLALCHEMY_DATABASE_URI (str): URI базы данных SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Флаг отслеживания изменений SQLAlchemy.
    """
    AUTHORIZATION_PASS = os.getenv("AUTHORIZATION_PASS")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False