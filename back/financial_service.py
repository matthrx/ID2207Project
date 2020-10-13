from .auth import managers_authentication_authorization
from .config import db, app
from .models import Application, FinancialRequest, DepartmentRecruitment
from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError

import json


@app.route("/financial_request/")
@managers_authentication_authorization
def create_financial_request(*args):
    decoded_request = json.loads(request.data.decode())
    project_id = decoded_request.get("project_reference")
    project = Application.query.filter(
        Application.project_reference == project_id
    ).count()
    if not project:
        return {
                   "error": "Project not found "
               }, 400
    financial_request = FinancialRequest(
        request_department=eval("DepartmentRecruitment.{}".format(decoded_request.get("request_department"))),
        project_reference=decoded_request.get("project_reference"),
        required_amount=int(decoded_request.get("required_amount")),
        reason=decoded_request.get("reason", "No reason was indicated")
    )
    try:
        db.session.add(financial_request)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
            "error": e.__dict__["orig"]
        }, 400