from flask import Flask
from back.config import app, db
from back.models import User, Roles

@app.route("/")
def test():
    return "App Working"


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    user = User(username="matthieu", role=Roles.FM, password="password")
    db.session.add(user)
    db.session.commit()
    app.run(port=8080)