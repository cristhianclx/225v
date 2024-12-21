from flask import Flask
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    def get(self):
        return {'status': 'OK'}


class PokemonByNameResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        if not raw.ok:
            return {}, 404
        data = raw.json()
        abilities = []
        for x in data["abilities"]:
            abilities.append(x["ability"]["name"])
        forms = []
        for x in data["forms"]:
            forms.append(x["name"])
        return {
            "name": name,
            "height": data["height"],
            "weight": data["weight"],
            "abilities": abilities,
            "forms": forms
        }


class IPInfoResource(Resource):
    def get(self):
        r = requests.get("https://ipinfo.io")
        r_data = r.json()
        return {
            "IP": r_data["ip"],
        }


class ExchangeResource(Resource):
    def get(self):
        r = requests.get("https://cuantoestaeldolar.pe/")
        r_source_code = r.text
        r_soup = BeautifulSoup(r_source_code, 'html.parser')
        r_elements = r_soup.find_all("div", class_="ValueQuotation_valueContainer__eH4KL")
        exchange_sale = r_elements[6].text
        exchange_buy = r_elements[7].text
        return {
            "EUR": {
                "sale": float(exchange_sale),
                "buy": float(exchange_buy)
            }
        }


api.add_resource(IndexResource, '/')
api.add_resource(PokemonByNameResource, '/pokemon/<name>')
api.add_resource(IPInfoResource, '/IP/')
api.add_resource(ExchangeResource, '/exchange/EUR/')