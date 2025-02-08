from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """
    Создает и настраивает Flask приложение.
    """
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Task
    from .routes import tasks_bp

    """
    Обработчики ошибок со стороны клиента.
    """
    @app.errorhandler(415)
    def unsupported_media_type(e):
        """
        Обрабатывает ошибку 415 (Unsupported Media Type).
        """
        return jsonify(error="Unsupported Media Type: Content-Type must be application/json"), 415

    @app.errorhandler(404)
    def endpoint_not_found(e):
        """
        Обрабатывает ошибку 404 (Endpoint Not Found).
        """
        return jsonify(str(e)), 404

    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    return app