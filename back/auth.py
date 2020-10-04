from back.config import app, db
from back.models import User, Roles

from flask_httpauth import HTTPBasicAuth
from flask import Response, request
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

import jwt

auth = HTTPBasicAuth()


#implemented as @token_required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'x-access-token' in request.headers:
            token = request.headers["Authorization"].split("Bearer")[1]
            if not token:
                return {"error" : "Token is missing"},401
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
                _ = User.query.filter_by(id=data['id']).first()
            except:
                return {"error": "Token not found"}, 401

            return f(*args, **kwargs)
        else:
            return {"error": "Not appropriate headers"}, 401

    return decorated


@app.route("/authenticate/", methods=['GET'])
@auth.verify_password
def authenticate():
    username, password = request.form["username"], request.form["password"]
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


@token_required
@app.route("/connected/")
def connected():
    return {"valid": "If you see this message, you're connected"}, 200


# Debugging tool, so far not an endpoint
def add_user(username, password, role: Roles):
    user = User(username=username, password=password, role=role)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        return str(e.__dict__["orig"])
