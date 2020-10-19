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
    user = User(username="matthieu", role=Roles.SCSO, password="password")
    db.session.add(user)
    user_nd = User(username="alicia", role=Roles.CSO, password="password")
    db.session.add(user_nd)
    user_rd = User(username="karl", role=Roles.FM, password="password")
    db.session.add(user_rd)
    user_fr = User(username="jack", role=Roles.PM, password="password")
    db.session.add(user_fr)
    user_fi = User(username="natalie", role=Roles.SM, password="password")
    db.session.add(user_fi)
    user_si = User(username="adam", role=Roles.PS, password="password")
    db.session.add(user_si)
    user_sv = User(username="chris", role=Roles.SS, password="password")
    db.session.add(user_sv)
    user_ei = User(username="simon", role=Roles.HR, password="password")
    db.session.add(user_ei)
    user_ni = User(username="mike", role=Roles.ADMIN, password="password")
    db.session.add(user_ni)
    db.session.commit()
    app.run(port=8080)