import datetime
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"
app.config["JWT_SECRET_KEY"] = "code"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(10), nullable=True)
    language = db.Column(db.String(2), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    raw = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageBasicSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "content",
            "priority",
        )
        model = Message


message_basic_schema = MessageBasicSchema()
messages_basic_schema = MessageBasicSchema(many = True)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "cristhian" or password != "123456":
        return {"msg": "Bad username or password"}, 401
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}


@app.route("/public")
def public():
    return {
        "is_public": True
    }


# header: Authorization: Bearer JWT
@app.route("/private", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {
        "is_public": False,
        "logger_user": current_user,
    }


@app.route("/messages", methods=["GET"])
@jwt_required()
def get_messages():
    current_user_first_name = get_jwt_identity()
    user = User.query.filter_by(first_name = current_user_first_name).first()
    if user:
        items = Message.query.filter_by(user = user).all()
        return messages_basic_schema.dump(items)
    return []