from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

api = Api(app)


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


class UserBasicSchema(ma.Schema):
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "age",
        )
        model = User


user_basic_schema = UserBasicSchema()
users_basic_schema = UserBasicSchema(many = True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "age",
            "location",
            "country",
            "language",
            "created_at",
        )
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class IndexResource(Resource):
    def get(self):
        return {
            "working": "OK"
        }


class UsersPublicResource(Resource):
    def get(self):
        items = User.query.all()
        return users_basic_schema.dump(items)


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)
    
    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item), 201


class UserIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)
    
    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        item.first_name = data.get("first_name", item.first_name)
        item.last_name = data.get("last_name", item.last_name)
        item.age = data.get("age", item.age)
        item.location = data.get("location", item.location)
        item.country = data.get("country", item.country)
        item.language = data.get("language", item.language)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item)
    
    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "content": item.content,
                "raw": item.raw,
                "priority": item.priority,
                "user_id": item.user_id,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return data

    def post(self):
        data = request.get_json()
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "content": item.content,
            "raw": item.raw,
            "priority": item.priority,
            "user_id": item.user_id,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }, 201


class MessageIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return {
            "id": item.id,
            "content": item.content,
            "raw": item.raw,
            "priority": item.priority,
            "user_id": item.user_id,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def patch(self, id):
        item = Message.query.get_or_404(id)
        data = request.get_json()
        item.content = data.get("content", item.content)
        item.raw = data.get("raw", item.raw)
        item.priority = data.get("priority", item.priority)
        item.user_id = data.get("user_id", item.user_id)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "content": item.content,
            "raw": item.raw,
            "priority": item.priority,
            "user_id": item.user_id,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def delete(self, id):
        item = Message.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


api.add_resource(IndexResource, "/")
api.add_resource(UsersPublicResource, "/users-public/")
api.add_resource(UsersResource, "/users/")
api.add_resource(UserIDResource, "/users/<int:id>")
api.add_resource(MessagesResource, "/messages/") # change serializers
api.add_resource(MessageIDResource, "/messages/<int:id>") # change serializers