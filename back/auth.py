from back.config import app, db
from back.models import User, Roles
from typing import List, Union
from flask import request
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
                return f(user.role, *args, **kwargs)
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


classic_authentication = partial(is_authenticated_and_authorized, roles=None)
fm_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.FM, Roles.ADMIN])
cso_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.CSO, Roles.ADMIN])
review_authentication_authorization = partial(is_authenticated_and_authorized, roles=[Roles.SCSO, Roles.FM, Roles.AM,
                                                                                      Roles.ADMIN])


@app.route("/connected/")
@classic_authentication
def connected(cur_roles):
    return {"valid": "If you see this message, you're connected as {}".format(cur_roles.name)}, 200


@app.route("/authorized_FM/")
@fm_authentication_authorization
def authorized():
    """

    :param cur_role: cur_role of the user
    :return: 400 if pb or 200 if ok
    """
    return {"valid": "You can only see this message if you are FM or ADMIN"}, 200


# Debugging tool, so far not an endpoint
def add_user(username, password, role: Roles):
    user = User(username=username, password=password, role=role)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        return str(e.__dict__["orig"])
