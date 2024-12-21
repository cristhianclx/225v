from flask import Flask
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    def get(self):
        return {'status': 'OK'}


class PokemonByNameResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        data = raw.json()
        return {
            "name": name,
            "height": data["height"],
            "weight": data["weight"],
            "abilities": [], # fill this 
            "forms": [] # fill this
        }


api.add_resource(IndexResource, '/')
api.add_resource(PokemonByNameResource, '/pokemon/<name>')