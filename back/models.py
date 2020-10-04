from back.config import app, db
from back.utils import generate_uuid, generate_date
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

import enum


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
        self.hash_password(password)
        self.last_connection_date = generate_date()
        if role: self.role = role

    def __repr__(self):
        return f'Id: {self.id} - Username: {self.username}'

    def hash_password(self, password):
        self.password_hashed = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hashed)

    def generate_auth_token(self, expiration=900):
        token_serialized = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        return token_serialized.dumps(
            {
                'token': self.id,
                "expiration": expiration
            }
        )

    @staticmethod
    def verify_token_content(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
