from back.config import app, db
from back.models import User, Roles
from flask_httpauth import HTTPBasicAuth
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

auth = HTTPBasicAuth()

@app.route("/authenticate")
@auth.verify_password
def authenticate(username, password):
    user = User(username=username, password=password)
    matching = User.query.filter(User.username == user.username, User.password_hashed == user.password_hashed).first()
    if not matching:
        return Response(
            {
                "error": "Wrong credentials"
            }, status=401
        )
    else:
        return Response(
            matching[0].generate_auth_token, status=200
        )


# Debugging tool, so far not an endpoint
def add_user(username, password, role: Roles):
    user = User(username=username, password=password, role=role)
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        return str(e.__dict__["orig"])

