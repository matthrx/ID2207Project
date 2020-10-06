from back.auth import cso_authentication_authorization, review_authentication_authorization
from back.config import db, app
from back.models import EventCreation, PreferencesEvent, Roles, Status
from flask import request, Response, jsonify
from sqlalchemy.exc import SQLAlchemyError


@app.route("/event_creation/", methods=["POST"])
@cso_authentication_authorization
def event_creation():
    event_create = EventCreation(
        client_name=request.form.get("client_name"),
        event_type=request.form.get("event_type"),
        from_date=request.form.get("from_date"),
        to_date=request.form.get("to_date"),
        expected_number_attendees=int(request.form.get("expected_number_attendees")),
        preferences=PreferencesEvent.__members__[request.form.get("preferences")]
    )
    try:
        db.session.add(event_create)
        db.session.commit()
        return Response(status=200)
    except SQLAlchemyError as e:
        return {
                   "error": e.__dict__["orig"]
               }, 400


@app.route("/review_event_creation/", methods=["UPDATE", "GET", "DELETE"])
@review_authentication_authorization
def review_event_creation(cur_role: Roles):
    if request.method == "GET":
        status_expected = eval("Status.pending_{}".format(cur_role.name))
        current_event_request_related = EventCreation.query.filter(
            EventCreation.status == status_expected
        )
        return jsonify(json_list=current_event_request_related.all())
    elif request.method == "UPDATE":
        # in this request user will be sending record_number (done automatically ;) )
        current_event_request_related = EventCreation.query.filter(
            EventCreation.record_number == int(request.form["record_number"])
        ).first()
        if request.form.get("feedback"):
            current_event_request_related.update(dict(
                feedback_fm=request.form.get("feedback", "No feedback added")
            ))
        next_status = eval("Status.pending_{}.next()".format(cur_role.name)) \
            if not request.form.get("dismissed") else Status.dismissed
        current_event_request_related.update(dict(
            status=next_status
        ))
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
    else:
        if cur_role == Roles.FM:
            return Response(status=401)
        event_request_to_delete = EventCreation.query.filter(
            EventCreation.record_number == int(request.form["record_number"])
        )
        try:
            db.session.delete(event_request_to_delete)
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400
