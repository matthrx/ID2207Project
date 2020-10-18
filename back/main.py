import back.auth
import back.event
import back.tasks
import back.staff_recruitment
import back.financial_service

# ------------ DO NOT DELETE THE LINES BEFORE ---------


from back.config import app, db
from back.models import User, Roles
from flask import Response


@app.route("/health/")
def health():
    return Response(status=200)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    user = User(username="matthieu", role=Roles.FM, password="password")
    db.session.add(user)
    user_nd = User(username="alicia", role=Roles.CSO, password="password")
    db.session.add(user_nd)
    db.session.commit()
    app.run(port=8080)