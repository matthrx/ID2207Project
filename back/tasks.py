from back.auth import (
                        managers_authentication_authorization,
                        product_service_authentication_authorization
                      )
from back.config import app, db
from back.models import Application, Priority, Tasks, User, RequestStatus
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
        assign_to_user=decode_request.get("user_assigned"),
        priority=eval("Priority.{}".format(decode_request.get("priority").lower()))
    )
    try:
        db.session.add(task)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
            "error": str(e.__dict__["orig"])
        }, 400


@app.route("/retrieve_task/", methods=["GET", "PUT", "DELETE"])
@product_service_authentication_authorization
def retrieve_task(user: User):
    decoded_request = json.loads(request.data.decode())
    if request.method == "GET":
        project_reference = decoded_request.get("project_reference")
        if not project_reference:
            specific_task = Tasks.query.filter(
                Tasks.assign_to_user == user.username
            ).all()
            return {"tasks": [task.to_dict() for task in specific_task]}, 200
        tasks = Tasks.query.filter(
            Tasks.assign_to_user == user.username,
            Tasks.project_reference == project_reference
        ).all()
        return {
            "project_reference": project_reference,
            "tasks": [task.to_dict() for task in tasks]
        }, 200
    elif request.method == "PUT":
        new_status = decoded_request.get("status")
        task_concerned = decoded_request.get("task_id")
        if not new_status or not task_concerned:
            return {
                "error": "Missing information (id or new status)"
            }, 400
        if new_status.lower() not in RequestStatus.__members__:
            return {
                       "error": "Status not recognized"
                   }, 400
        task_concerned = Tasks.query.filter(
            Tasks.task_id == task_concerned
        ).first()
        task_concerned.status = eval("RequestStatus.{}".format(new_status))
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": str(e.__dict__["orig"])
                   }, 400
        # either suspended or done or dismissed
    elif request.method == "DELETE":
        task_id = decoded_request.get("task_id")
        if not task_id:
            return {
                "error": "No task id, required for deletion"
            }, 400
        task_to_delete = Tasks.query.filter(
            Tasks.task_id == task_id,
            Tasks.status == RequestStatus.dismissed
        ).first()
        if not task_to_delete:
            return {
                "error": "id not recognized"
            }, 401
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                "error": str(e.__dict__["orig"])
            }, 400
