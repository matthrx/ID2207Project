from back.config import app, db
from back.models import User, Roles
from typing import List, Union
from flask import request, Response
from functools import wraps, partial
from sqlalchemy.exc import SQLAlchemyError

import jwt, json


# implemented as @token_required
def is_authenticated_and_authorized(f, roles: Union[List[Roles], None]):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split("Bearer")[1].replace(" ", "")
            if not token:
                return {"error": "Token is missing"}, 401
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
                user = User.query.filter_by(id=data['id']).first()
                if not user:
                    return {
                        "error": "User not found "
                    }, 401
                if roles:
                    if user.role not in roles:
                        return {
                            "error": "Not authorized to have access to this resource"
                        }, 403
                return f(user, *args, **kwargs)
            except (jwt.ExpiredSignature, jwt.InvalidTokenError):  # expired signature we're suppose to resend a new token
                return {"error": "Problem of token "}, 401
        else:
            return {"error": "Not appropriate headers"}, 401

    return decorated


@app.route("/authenticate/", methods=['GET'])
def authenticate():
    decoded_request = json.loads(request.data.decode())
    username, password = decoded_request["username"], decoded_request["password"]
    matching = User.query.filter(User.username == username).first()
    are_credentials_ok = matching.verify_password(password) if matching else False
    if not are_credentials_ok:
        return (
            {
                "error": "Wrong credentials"
            }, 401
        )
    else:
        return matching.generate_auth_token(), 200


classic_authentication = partial(is_authenticated_and_authorized, roles=list(Roles.__dict__["_member_map_"].values()))
fm_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.FM, Roles.ADMIN])
cso_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.CSO, Roles.ADMIN])
scso_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.SCSO, Roles.ADMIN])
review_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.SCSO, Roles.FM, Roles.AM,
                                                                           Roles.ADMIN])
admin_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.ADMIN])
managers_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.PM, Roles.SM, Roles.ADMIN])
product_service_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.SM, Roles.PM, Roles.PS, Roles.SS, Roles.ADMIN])
hr_managers_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.HR, Roles.PM, Roles.SM, Roles.ADMIN])
fm_managers_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.PM, Roles.SM, Roles.FM, Roles.ADMIN])


@app.route("/connected/")
@classic_authentication
def connected(user: User):
    return {"valid": "If you see this message, you're connected as {}".format(user.username)}, 200


@app.route("/authorized_FM/")
@fm_authentication_authorization
def authorized(*args):
    """
    :return: 400 if pb or 200 if ok
    """
    return {"valid": "You can only see this message if you are FM or ADMIN"}, 200


@app.route("/change_password/", methods=["PUT"])
@classic_authentication
def change_password(user: User):
    decoded_request = json.loads(request.data.decode())
    if not decoded_request.get("new_password"):
        return Response(status=400)
    user_concerned = User.query.filter_by(
        User.id == user.id
    ).first()
    if user_concerned:
        user_concerned.password = decoded_request.get("new_password")
        try:
            db.session.commit()
            return Response(status=200)
        except SQLAlchemyError as e:
            return {
                       "error": e.__dict__["orig"]
                   }, 400


@app.route("/create_user/", methods=["POST"])
@admin_authentication_authorization
def add_user(*args):
    decoded_data = json.loads(request.data.decode())
    user = User(username=decoded_data.get("username"),
                password=decoded_data.get("password"),
                role=eval("Roles.{}".format(decoded_data.get("role").lower()))
                )
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        return {
            "error": e.__dict__["orig"]
        }, 400
