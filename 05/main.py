from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(10), nullable=True)
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


class IndexResource(Resource):
    def get(self):
        return {
            "working": "OK"
        }


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "age": item.age,
                "location": item.location,
                "country": item.country,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return data

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
            "location": item.location,
            "country": item.country,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }, 201


class UserIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(1)
        return {
            "id": item.id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
            "location": item.location,
            "country": item.country,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def patch(self, id):
        item = User.query.get_or_404(1)
        data = request.get_json()
        item.first_name = data.get("first_name", item.first_name)
        item.last_name = data.get("last_name", item.last_name)
        item.age = data.get("age", item.age)
        item.location = data.get("location", item.location)
        item.country = data.get("country", item.country)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "age": item.age,
            "location": item.location,
            "country": item.country,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def delete(self, id):
        item = User.query.get_or_404(1)
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


api.add_resource(IndexResource, "/")
api.add_resource(UsersResource, "/users/")
api.add_resource(UserIDResource, "/users/<int:id>")
api.add_resource(MessagesResource, "/messages/")

# /messages/<id> GET, PATCH, DELETE