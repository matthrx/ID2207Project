from back.auth import (
                        managers_authentication_authorization,
                        product_service_authentication_authorization
                      )
from back.config import app, db
from back.models import Application, Priority, Tasks, User
from back.utils import generate_uuid
from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError
import json


@app.route('/create_task/', methods=['POST'])
@managers_authentication_authorization
def create_task(*args):
    decode_request = json.loads(request.data.decode())
    project_id = decode_request.get("project_reference")
    project = Application.query.filter(
        Application.project_reference == project_id
    ).count()
    if not project:
        return {
            "error": "Project not found "
        }, 400
    user_assigned = User.query.filter(
        User.username == decode_request.get("user_assigned")
    )
    if not user_assigned:
        return {
            "error": "User assigned not found"
        }
    task = Tasks(
        task_id=generate_uuid(),
        project_reference=project_id,
        description=decode_request.get("description"),
        assign_to_user=user_assigned,
        priority=eval("Priority.{}".format(decode_request.get("priority").lower()))
    )
    try:
        db.session.add(task)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
            "error": e.__dict__["orig"]
        }, 400


@app.route("/retrieve_task/", methods=["GET", "DELETE"])
@product_service_authentication_authorization
def retrieve_task(*args):
    decoded_request = json.loads(request.data.decode())
    if request.method == "GET":
        if decoded_request.get("task_id"):
            specific_task = Tasks.query.filter(
                Tasks.task_id == decoded_request.get("task_id")
            ).all()
            if not specific_task:
                return {
                    "error": "No task found for this specific id"
                }, 400
            return specific_task, 200
        project_reference = decoded_request.get("project_reference")
        if not project_reference:
            return {
                "error": "Indicate project reference"
            }, 400
        tasks = Tasks.query.filter(
            Tasks.project_reference == project_reference
        ).all()
        return {
            "project_reference": project_reference,
            "tasks": [task.to_dict() for task in tasks]
        }, 200
    elif request.method == "DELETE":
        task_id = decoded_request.get("task_id")
        if not task_id:
            return {
                "error": "No task id, required for deletion"
            }, 400
        task_to_delete = Tasks.query.filter(
            Tasks.task_id == task_id
        )
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                "error": e.__dict__["orig"]
            }, 400
