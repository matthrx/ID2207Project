from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "dcec80bc44a48b35a8c52ff7928624b7ef889f49489d12de90ee3dc63e66ab14"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/projectID2207.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

