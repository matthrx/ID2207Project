from .auth import (
    managers_authentication_authorization,
    fm_managers_authentication_authorization
)
from .config import db, app
from .models import Application, FinancialRequest, DepartmentRecruitment,\
    RequestStatus, User, Roles
from .utils import generate_uuid
from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError

import json


@app.route("/create_financial_request/", methods=["POST"])
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
    financial_request_id = generate_uuid()
    financial_request = FinancialRequest(
        financial_request_id=financial_request_id,
        request_department=eval("DepartmentRecruitment.{}".format(decoded_request.get("request_department"))),
        project_reference=decoded_request.get("project_reference"),
        required_amount=int(decoded_request.get("required_amount")),
        reason=decoded_request.get("reason", "No reason was indicated"),
    )
    try:
        db.session.add(financial_request)
        db.session.commit()
        return {"financial_request_id": financial_request_id}, 200
    except SQLAlchemyError as e:
        return {
            "error": e.__dict__["orig"]
        }, 400


@app.route("/review_financial_request/", methods=["GET", "PUT", "DELETE"])
@fm_managers_authentication_authorization
def review_financial_request(user: User):
    decoded_request = json.loads(request.data.decode())
    if request.method == "GET":
        if decoded_request.get("financial_request_id"):
            financial_request = FinancialRequest.query.filter(
                FinancialRequest.financial_request_id == decoded_request.get("financial_request_id")
            ).first()
            return financial_request.to_dict(), 200
        elif decoded_request.get("project_reference"):
            financial_request = FinancialRequest.query.filter(
                FinancialRequest.project_reference == decoded_request.get("project_reference")
            ).all()
            return {
                "financial_requests": [each_f_request.to_dict() for each_f_request in financial_request]
            }, 200
        financial_requests = FinancialRequest.query.all()
        return { "financial_requests": [each_f_request.to_dict() for each_f_request in financial_requests]}, 200
    elif request.method == "PUT":
        if user.role not in [Roles.FM, Roles.ADMIN]:
            return Response(status=401)
        request_id = decoded_request.get("financial_request_id")
        if not request_id:
            return {
                "error": "No id given"
            }, 400
        financial_req_concerned = FinancialRequest.query.filter(
            FinancialRequest.financial_request_id == request_id,
            FinancialRequest.status == RequestStatus.ongoing
        ).first()
        if not financial_req_concerned:
            return {
                "error": "id not recognized"
            }, 400
        financial_req_concerned.status = RequestStatus.done \
            if decoded_request.get("status").lower() != "dismissed" \
            else RequestStatus.dismissed
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
    else:
        request_id = decoded_request.get("financial_request_id")
        if not request_id:
            return {
                       "error": "No id given"
                   }, 400
        financial_req_concerned = FinancialRequest.query.filter(
            FinancialRequest.financial_request_id == request_id,
            FinancialRequest.status == RequestStatus.ongoing
        ).first()
        if not financial_req_concerned:
            return {
                "error": "This request is not being currently handled or id is wrong"
            }, 400
        try:
            db.session.delete(financial_req_concerned)
            db.session.commit()
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
