from back.config import app, db
from back.utils import generate_uuid, generate_date
from flask import jsonify
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy_serializer import SerializerMixin
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


class Priority(enum.Enum):
    very_high = 0,
    high = 1,
    medium = 2,
    low = 3,
    very_low: 4


class RequestStatus(enum.Enum):
    ongoing = 0,
    dismissed = 1,
    done = 2,
    suspended = 3


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


class DepartmentRecruitment(enum.Enum):
    administration = 0,
    services = 1,
    production = 2,
    financial = 3


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(50))
    password_hashed = db.Column(db.String(128))  # hashed password
    last_connection_date = db.Column(db.String(20))
    role = db.Column(db.Enum(Roles))
    tasks = db.relationship("Tasks")

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

    def generate_auth_token(self, expire=3600):
        token = jwt.encode({'id': self.id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(seconds=expire)},
                           app.config["SECRET_KEY"])
        return jsonify(
            {
                'token': token.decode("utf-8"),
                "username": self.username,
                "expiration": expire,
                'role': self.role.name
            }
        )


class EventCreation(db.Model, SerializerMixin):
    # no client record (won't be a table)
    __tablename__ = "Event"
    record_number = db.Column(db.String, primary_key=True)
    client_name = db.Column(db.String(100))
    event_type = db.Column(db.String(100))
    from_date = db.Column(db.String(50))  # expecting dd/mm/yyyy
    to_date = db.Column(db.String(50))
    expected_number_attendees = db.Column(db.Integer)
    preferences = db.Column(db.Enum(PreferencesEvent), nullable=True)
    feedback_fm = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(Status), default=Status.pending_SCSO)

    def to_dict(self, only=(), rules=(),
                date_format=None, datetime_format=None, time_format=None, tzinfo=None,
                decimal_format=None, serialize_types=None):
        return {
            "record_number": self.record_number,
            "client_name": self.client_name,
            "event_type": self.event_type,
            "from_date": self.from_date,
            'to_date': self.to_date,
            "expected_number_attendees": self.expected_number_attendees,
            "preferences": self.preferences.name,
            "feedback_fm": self.feedback_fm,
            "status": self.status.name
        }


class Application(db.Model, SerializerMixin):
    __tablename__ = "Application"
    project_reference = db.Column(db.String, primary_key=True)
    client_record_number = db.Column(db.Integer, primary_key=True, default=1)
    client_name = db.Column(db.String(100))
    event_type = db.Column(db.String(100))
    description = db.Column(db.String)
    from_date = db.Column(db.String(50))  # expecting dd/mm/yyyy
    to_date = db.Column(db.String(50))
    expected_number_attendees = db.Column(db.Integer)
    planned_budget = db.Column(db.Float)
    tasks = db.relationship("Tasks")
    decorations = db.Column(db.String(), default=str())
    food_drinks = db.Column(db.String(), default=str())
    filming_photos = db.Column(db.String(), default=str())
    music = db.Column(db.String(), default=str())
    posters_art_work = db.Column(db.String(), default=str())
    computer_related_issues = db.Column(db.String(), default=str())
    other_needs = db.Column(db.String(), default=str())

    def to_dict(self, only=(), rules=(),
                date_format=None, datetime_format=None, time_format=None, tzinfo=None,
                decimal_format=None, serialize_types=None):
        return {
            "project_reference": self.project_reference,
            "record_number": self.client_record_number,
            "client_name": self.client_name,
            "event_type": self.event_type,
            "description": self.description,
            "from_date": self.from_date,
            'to_date': self.to_date,
            "expected_number_attendees": self.expected_number_attendees,
            "planned_budget": self.planned_budget,
            "application_details": {
                "decorations": self.decorations,
                "food_drinks": self.food_drinks,
                "filming_photos": self.filming_photos,
                "music": self.music,
                "poster_art_work": self.posters_art_work,
                "computer_related_issues": self.computer_related_issues,
                "other_needs": self.other_needs
            }
        }


class Tasks(db.Model, SerializerMixin):
    __tablename__ = "Tasks"
    task_id = db.Column(db.String(30), name="id_task", primary_key=True, default="0000-000-000")
    project_reference = db.Column(db.String(), db.ForeignKey("Application.project_reference"), unique=False)
    description = db.Column(db.String())
    assign_to_user = db.Column(db.String(), db.ForeignKey("User.username"))
    priority = db.Column(db.Enum(Priority), default=Priority.medium)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.ongoing)

    def to_dict(self, only=(), rules=(),
                date_format=None, datetime_format=None, time_format=None, tzinfo=None,
                decimal_format=None, serialize_types=None):
        return {
            "task_id": self.task_id,
            "project_reference": self.project_reference,
            "description": self.description,
            "assign_to_user": self.assign_to_user,
            "priority": self.priority.name,
            "status": self.status.name
        }


class StaffRecruitment(db.Model, SerializerMixin):
    __tablename__ = "Staff"
    staff_request_id = db.Column(db.String, primary_key=True)
    is_full_time = db.Column(db.Boolean)
    request_department = db.Column(db.Enum(DepartmentRecruitment))
    year_experience_min = db.Column(db.Integer)
    job_title = db.Column(db.String(200))
    job_description = db.Column(db.String(500))
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.ongoing)

    def to_dict(self, only=(), rules=(),
                date_format=None, datetime_format=None, time_format=None, tzinfo=None,
                decimal_format=None, serialize_types=None):
        return {
            "staff_request_id": self.staff_request_id,
            "is_full_time": self.is_full_time,
            "department": self.request_department.name,
            "years_min": self.year_experience_min,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "status": self.status.name
        }


class FinancialRequest(db.Model, SerializerMixin):
    __tablename__ = "FinancialRequest"
    financial_request_id = db.Column(db.String, primary_key=True)
    request_department = db.Column(db.Enum(DepartmentRecruitment))
    project_reference = db.Column(db.String(), db.ForeignKey("Application.project_reference"), unique=False)
    required_amount = db.Column(db.Integer)
    reason = db.Column(db.String(500))
    status =db.Column(db.Enum(RequestStatus), default=RequestStatus.ongoing)

    def to_dict(self, only=(), rules=(),
                date_format=None, datetime_format=None, time_format=None, tzinfo=None,
                decimal_format=None, serialize_types=None):
        return {
            "financial_request_id": self.financial_request_id,
            "request_department": self.request_department.name.upper(),
            "project_reference": self.project_reference,
            "required_amount": self.required_amount,
            "reason": self.reason,
            "status": self.status.name
        }