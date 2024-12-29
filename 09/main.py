from flask import Flask, render_template, request, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Room(db.Model):
    
    __tablename__ = "rooms"
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    max_participants = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Room: {}>".format(self.id)


class Message(db.Model):
    
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    room_id = db.Column(db.String, db.ForeignKey("rooms.id"))
    room = db.relationship("Room", backref="room")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "nickname",
            "content",
            "created_at"
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/ping/")
def ping():
    return {
        "status": "live"
    }


@app.route("/")
def index():
    data = Room.query.all()
    return render_template("index.html", items = data)


@app.route("/rooms/create/", methods=["GET", "POST"])
def rooms_create():
    if request.method == "GET":
        return render_template("rooms-create.html")
    if request.method == "POST":
        item = Room(**request.form)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('rooms_by_id', id=item.id))


@app.route("/r/<id>/")
def rooms_by_id(id):
    room = Room.query.get_or_404(id)
    participants = len(db.session.query(Message.nickname, db.func.count(Message.nickname)).filter(Message.room_id == room.id).group_by(Message.nickname).all())
    if room.max_participants <= participants:
        print("max participants: {}, participants: {}".format(room.max_participants, participants))
        return redirect(url_for('index'))
    messages = Message.query.filter_by(room = room)
    return render_template("messages.html", room=room, messages=messages)


@socketio.on("ws-messages")
def handle_ws_messages(data):
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    data_to_send = message_schema.dump(item)
    channel_id = "ws-messages-{}".format(item.room_id)
    socketio.emit(channel_id, data_to_send)