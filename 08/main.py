from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app)


class Message(db.Model):
    
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # importance = db.Column(db.String(10), nullable=False, default="LOW") # LOW, HIGH
    # details # String(200)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message: {}>".format(self.id)


@app.route("/ping/")
def ping():
    return {
        "status": "live"
    }


@app.route("/")
def index():
    data = Message.query.all()
    return render_template("index.html", messages=data)


@socketio.on("ws-welcome")
def handle_ws_welcome(data):
    print("ws-welcome: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data):
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    socketio.emit("ws-messages-responses", data)


# LABORATORIO
# el chat que manejamos incluya los campos, importance y details