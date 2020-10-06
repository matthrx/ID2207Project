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
    PS = 8,
    ADMIN = 9


class PreferencesEvent(enum.Enum):
    decorations = 0,
    parties = 1,
    photos_filming = 2
    breakfast_launch_dinner = 3,
    drinks = 4


class Status(enum.Enum):
    pending_SCSO = 0,
    pending_FM = 1,
    pending_AM = 2,
    validated = 3
    dismissed = 4,

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1 if members.index(self) < 2 else members.index(self)
        return members[index]


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


class EventCreation(db.Model):
    # no client record (won't be a table)
    __tablename__ = "event_request"
    record_number = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, default=1)
    client_name = db.Column(db.String(100))
    event_type = db.Column(db.String(100))
    from_date = db.Column(db.String(50))  # expecting dd/mm/yyyy
    to_date = db.Column(db.String(50))
    expected_number_attendees = db.Column(db.Integer)
    preferences = db.Column(db.Enum(PreferencesEvent), nullable=True)
    feedback_fm = db.Column(db.String)
    status = db.Column(db.Enum(Status), default=Status.pending_SCSO)



