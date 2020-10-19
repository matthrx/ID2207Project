import json

from flask import request, Response
from sqlalchemy.exc import SQLAlchemyError

from back.auth import (cso_authentication_authorization,
                       review_authentication_authorization,
                       scso_authentication_authorization,
                       managers_authentication_authorization
                       )
from back.config import db, app
from back.models import (
    Application,
    EventCreation,
    PreferencesEvent,
    Roles,
    Status,
    User)
from back.utils import generate_uuid


# parser_event = {
#     "client_name": fields.String,
#     "event_type": fields.String,
#     "from_date": fields.String,
#     "to_date": fields.String,
#     "expected_number_attendees": fields.Integer,
#     "preferences": fields.String,
#     "feedback_fm": fields.String
# }


@app.route('/event_application_creation', methods=["POST"])
@scso_authentication_authorization
def event_application_creation(*args):
    decode_request = json.loads(request.data.decode())
    project_reference = generate_uuid()
    application_to_create = Application(
        project_reference=project_reference,
        client_record_number=decode_request.get("record_number"),
        client_name=decode_request.get("client_name"),
        event_type=decode_request.get("event_type"),
        description=decode_request.get("description"),
        from_date=decode_request.get("from_date"),
        to_date=decode_request.get("to_date"),
        expected_number_attendees=int(decode_request.get("expected_number_attendees")),
        planned_budget=int(decode_request.get("planned_budget")),
        decorations=decode_request.get("decorations"),
        food_drinks=decode_request.get("food_drinks"),
        filming_photos=decode_request.get("filming_photos"),
        music=decode_request.get("music"),
        posters_art_work=decode_request.get("posters_art_work"),
        computer_related_issues=decode_request.get("computer_related_issues"),
        other_needs=decode_request.get("other_needs")
    )
    try:
        db.session.add(application_to_create)
        db.session.commit()
        return {
            "project_reference": project_reference
        }, 200
    except SQLAlchemyError as e:
        return {
                   "error": e.__dict__["orig"]
               }, 400


@app.route("/event_application_retrieve/", methods=['GET'])
@managers_authentication_authorization
def application_retrieve(*args):
    # either the use indicate the application id or we retrieve all of them
    decoded_request = json.loads(request.data.decode())
    if decoded_request.get("application_id"):
        application_needed = Application.query.filter(
            Application.project_reference == decoded_request.get("application_id")
        ).first()
        if not application_needed:
            return {
                "error": "Application not found (wrong id)"
            }, 400
        return application_needed.to_dict(), 200
    else:
        applications = Application.query.all()
        return {"applications": [application.to_dict() for application in applications]}, 200


@app.route("/event_creation/", methods=["POST"])
@cso_authentication_authorization
def event_creation(*args):
    decode_request = json.loads(request.data.decode())
    event_create = EventCreation(
        record_number=generate_uuid(),
        client_name=decode_request.get("client_name"),
        event_type=decode_request.get("event_type"),
        from_date=decode_request.get("from_date"),
        to_date=decode_request.get("to_date"),
        expected_number_attendees=int(decode_request.get("expected_number_attendees")),
        preferences=PreferencesEvent.__members__[decode_request.get("preferences")]
    )
    try:
        db.session.add(event_create)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
                   "error": e.__dict__["orig"]
               }, 400


# @marshal_with(parser_event)
@app.route("/review_event_creation/", methods=["PUT", "GET", "DELETE"])
@review_authentication_authorization
def review_event_creation(user: User):
    if request.method == "GET":
        status_expected = eval("Status.pending_{}".format(user.role.name))
        current_event_request_related = EventCreation.query.filter(
            EventCreation.status == status_expected
        ).all()
        return {"events": [each_event.to_dict() for each_event in current_event_request_related]}, 200
    elif request.method == "PUT":
        decoded_request = json.loads(request.data.decode())
        # in this request user will be sending record_number (done automatically ;) )
        current_event_request_related = EventCreation.query.filter(
            EventCreation.record_number == decoded_request.get("record_number"),
            EventCreation.status == eval("Status.pending_{}".format(user.role.name))
        ).first()
        if not current_event_request_related:
            return {
                "error": "Request can't be fulfilled"
            }, 400
        if decoded_request.get("feedback"):
            current_event_request_related.feedback_fm = decoded_request.get("feedback", "No feedback")
            current_event_request_related.status = eval("Status.pending_{}.next()".format(user.role.name))
        if decoded_request.get("status"):
            current_event_request_related.status = eval("Status.pending_{}.next()".format(user.role.name)) \
                if decoded_request.get("status").lower() != "dismissed" else Status.dismissed
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
    else:
        decoded_request = json.loads(request.data.decode())
        if user.role == Roles.FM:
            return Response(status=401)
        event_request_to_delete = EventCreation.query.filter(
            EventCreation.record_number == decoded_request.get("record_number"),
            EventCreation.status == Status.dismissed
        ).first()
        if not event_request_to_delete:
            return {
                       "error": "request can't be fulfilled"
                   }, 400
        try:
            db.session.delete(event_request_to_delete)
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
