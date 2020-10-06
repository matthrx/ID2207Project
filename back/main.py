from back.config import app, db
import back.auth  # keep it
from back.models import User, Roles


@app.route("/health")
def health():
    return {"status": "Up"}, 200


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    user = User(username="matthieu", role=Roles.FM, password="password")
    db.session.add(user)
    user_nd = User(username="alicia", role=Roles.AM, password="password")
    db.session.add(user_nd)
    db.session.commit()
    app.run(port=8080)