from flask import Flask, render_template, request, redirect, url_for
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
    return render_template("index.html")


@app.route("/users")
def users():
    data = User.query.all()
    return render_template("users.html", items=data)


@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        user_first_name = request.form["first_name"]
        user_last_name = request.form["last_name"]
        user_age = request.form["age"]
        user_location = request.form["location"]
        user_country = request.form["country"]
        user = User(
            first_name=user_first_name,
            last_name=user_last_name,
            age=user_age,
            location=user_location,
            country=user_country
        )
        db.session.add(user)
        db.session.commit()
        return render_template("users-add.html", message="User added")


@app.route("/users/<id>")
def users_by_id(id):
    user = User.query.get_or_404(id)
    return render_template("users-detail.html", user=user)


@app.route("/users/edit/<id>", methods=["GET", "POST"])
def users_edit_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", user=user)
    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.age = request.form["age"]
        user.location = request.form["location"]
        user.country = request.form["country"]
        db.session.add(user)
        db.session.commit()
        return render_template("users-edit.html", user=user, message="User edited")


@app.route("/users/delete/<id>", methods=["GET", "POST"])
def users_delete_by_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", user=user)
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))


@app.route("/messages")
def messages():
    data = Message.query.all()
    return render_template("messages.html", items=data)


@app.route("/messages/add", methods=["GET", "POST"])
def messages_add():
    if request.method == "GET":
        return render_template("messages-add.html")
    if request.method == "POST":
        message_content = request.form["content"]
        message_priority = request.form["priority"]
        message = Message(
            content=message_content,
            priority=message_priority,
        )
        db.session.add(message)
        db.session.commit()
        return render_template("messages-add.html", message="Message added")


# /messages/1 # detalle de un mensaje
# /messages/edit/1 # editar un mensaje
# /messages/delete/1 # borrar un mensaje