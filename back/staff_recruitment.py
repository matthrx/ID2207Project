from .auth import managers_authentication_authorization
from .config import db, app
from .models import StaffRecruitment, DepartmentRecruitment

from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError

import json


@app.route("/staff_request/", methods=["POST"])
@managers_authentication_authorization
def create_staff_recruitement(*args):
    decoded_request = json.loads(request.data.decode())
    staff_request = StaffRecruitment(
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