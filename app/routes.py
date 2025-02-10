from flask import (
    Blueprint, redirect, render_template, request, abort, url_for, jsonify
)
import logging
from app import db
from .models import Task
from .validator import TaskValidator
from .serializer import TaskSerializer

tasks_bp = Blueprint("tasks", __name__)

"""
Основные маршруты API
"""

@tasks_bp.route("/", methods=["GET"])
def tasks_get_list():
    """
    Получает список всех задач.
    """
    # получаем все задачи из базы данных
    tasks = Task.query.all()

    # сериализуем задачи
    serialized_tasks = [TaskSerializer.serialize(task) for task in tasks]

    # логируем успешное получение списка задач
    logging.info("Task list sended")
    return jsonify(serialized_tasks), 200

@tasks_bp.route("/<int:task_id>", methods=["GET"])
def tasks_get_item(task_id):
    """
    Получает задачу по её идентификатору.
    """
    # получаем задачу по идентификатору
    task = db.session.get(Task, task_id)

    # если задача не найдена, возвращаем ошибку
    if not task:
        return jsonify(error="Task not found."), 404

    # сериализуем задачу
    serialized_tasks = TaskSerializer.serialize(task=task)

    # логируем успешное получение задачи
    logging.info("Task item sended")
    return jsonify(serialized_tasks), 200

@tasks_bp.route("/", methods=["POST"])
def tasks_post():
    """
    Создает новую задачу.
    """
    # получаем данные из запроса
    data = request.get_json()

    # валидируем данные
    try:
        TaskValidator.validate_post_data(data=data)

    except Exception as e:
        # логируем ошибку валидации
        logging.info("Validation failed", str(e))

        return jsonify(error=str(e)), 400

    # извлекаем данные из запроса
    title = data.get("title")
    status = data.get("status", "todo")

    # создаем новую задачу
    try:
        new_task = Task(
            title=title,
            status=status
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "msg": "Task created successfully",
            "properties": {
                "title": title,
                "status": status
            }
        }), 201

    except Exception as e:
        # откатываем изменения в случае ошибки
        db.session.rollback()
        logging.info("Validation failed", str(e))

        return jsonify(error=str(e))


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def task_delete(task_id):
    data = request.get_json()
    
    
    try:
        TaskValidator.validate_delete_data(data=data)
    
    except Exception as e:
        # логируем ошибку валидации
        logging.info("Validation failed", str(e))

        return jsonify(error=str(e)), 400
        
    task = db.session.get(Task, task_id)

    # если задача не найдена, возвращаем ошибку
    if not task:
        return jsonify(error="Task not found."), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        
        return jsonify(msg=f"Task with id {task_id} deleted successfuly."), 200

    except Exception as e:
        db.session.rollback()
        
        return abort(500)
    
    
@tasks_bp.route("/<int:task_id>", methods=["PATCH"])
def tasks_patch(task_id):
    """
    Обновляет статус задачи.
    """
    # получаем данные из запроса
    data = request.get_json()

    # валидируем данные
    try:
        TaskValidator.validate_patch_data(data=data)

    except Exception as e:
        return jsonify(error=str(e)), 400

    # извлекаем статус из данных
    status = data.get("status")
    task = db.session.get(Task, task_id)

    # если задача не найдена, возвращаем ошибку
    if not task:
        return jsonify(error="Task not found."), 404

    # обновляем статус задачи
    try:
        task.status = status
        db.session.commit()
        response = TaskSerializer.serialize(task=task)

        # логируем успешное обновление задачи
        logging.info("Task updated successfuly")

        return jsonify(response), 200

    except Exception as e:
        # откатываем изменения в случае ошибки
        db.session.rollback()
        logging.error("Error occurred while updating task: %s", str(e))

        return jsonify(error=str(e)), 400