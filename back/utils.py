import uuid
import datetime


def generate_uuid():
    return str(uuid.uuid4())


def generate_date():
    return datetime.datetime.now().strftime("%Y/%m/%d:%H:%M")

