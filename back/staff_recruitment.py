from .auth import (
        managers_authentication_authorization,
        hr_managers_authentication_authorization
        )
from .config import db, app
from .models import StaffRecruitment, DepartmentRecruitment, User, HRStatus, Roles
from .utils import generate_uuid

from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError

import json


@app.route("/create_staff_request/", methods=["POST"])
@managers_authentication_authorization
def create_staff_recruitment(*args):
    decoded_request = json.loads(request.data.decode())
    staff_request = StaffRecruitment(
        staff_request_id= generate_uuid(),
        is_full_time=bool(decoded_request.get("is_full_time")),
        request_department=eval("DepartmentRecruitment.{}".format(decoded_request.get("request_department").lower())),
        year_experience_min=int(decoded_request.get("year_experience_min", None)),
        job_title=decoded_request.get("job_title"),
        job_description=decoded_request.get("job_description")
    )
    try:
        db.session.add(staff_request)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
            "error": e.__dict__["orig"]
        }, 400


@app.route("/review_staff_request/", methods=["GET", "PUT", "DELETE"])
@hr_managers_authentication_authorization
def review_staff_request(user: User):
    decoded_request = json.loads(request.data.decode())
    # we'll suppose that managers can see all the requests and so can hr
    if request.method == "GET":
        if decoded_request.get("staff_request_id"):
            specific_staff_request = StaffRecruitment.query.filter(
                StaffRecruitment.staff_request_id == decoded_request
            ).first()
            return specific_staff_request.to_dict(), 200
        else:
            staff_requests = StaffRecruitment.query.all()
            return {
                "tasks": [staff_request.to_dict() for staff_request in staff_requests]
            }, 200
    elif request.method == "PUT":
        if not decoded_request.get("staff_request_id"):
            return {
                "error": "Need to indicate the staff request id"
            }, 400
        if user.role not in [Roles.HR, Roles.ADMIN]:
            return Response(status=401)
        current_staff_request = StaffRecruitment.query.filter(
            StaffRecruitment.staff_request_id == decoded_request.get("staff_request_id"),
            StaffRecruitment.status == HRStatus.ongoing
        )
        if not current_staff_request:
            return {
                "error": "No ongoing request with those parameters"
            }, 400
        current_staff_request.status = HRStatus.done if decoded_request.get("status").lower() == "done" \
            else HRStatus.dismissed
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
    else:
        if not decoded_request.get("staff_request_id"):
            return {
                "error": "Need to indicate the staff request id"
            }, 400
        to_delete = StaffRecruitment.query.filter(
            StaffRecruitment.staff_request_id == decoded_request.get("staff_request_id")
        )
        try:
            db.session.delete(to_delete)
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                   "error": e.__dict__["orig"]
               }, 400