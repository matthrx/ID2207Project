from back.config import app, db
from back.utils import generate_uuid, generate_date
from flask import jsonify
from passlib.apps import custom_app_context as pwd_context

import datetime
import enum
import jwt


class Roles(enum.Enum):
    CSO = 0,
    SCSO = 1,
    FM = 2,
    AM = 3,
    HR = 4,
    SM = 5,
    PM = 6,
    SS = 7,
    PS = 8


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(50))
    password_hashed = db.Column(db.String(128))  # hashed password
    last_connection_date = db.Column(db.String(20))
    role = db.Column(db.Enum(Roles))

    def __init__(self, username, password, role=None):
        self.id = generate_uuid()
        self.username = username
        self.password_hashed = pwd_context.encrypt(password)
        self.last_connection_date = generate_date()
        if role: self.role = role

    def __repr__(self):
        return f'Id: {self.id} - Username: {self.username}'

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hashed)

    def generate_auth_token(self, expire=900):
        token = jwt.encode({'id': self.id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(seconds=expire)},
                           app.config["SECRET_KEY"])
        return jsonify(
            {
                'token': token.decode("utf-8"),
                "username": self.username,
                "expiration": expire
            }
        )



