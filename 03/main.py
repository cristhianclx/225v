from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@127.0.0.1:5432/bbdd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    location = db.Column(db.String(50))
    country = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    priority = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message: {}>".format(self.id)


@app.route("/status")
def status():
    return {
        "status": "ok"
    }


@app.route("/")
def index():
    return {}


@app.route("/users")
def users():
    data = User.query.all()
    return render_template("users.html", items=data)

# /messages
# /users/add