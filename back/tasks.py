from back.auth import managers_authentication_authorization
from back.config import app, db
from back.models import Application, Priority, Tasks, User
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