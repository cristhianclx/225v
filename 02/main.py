from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/status")
def status():
    return {
        "status": "ok"
    }

@app.route("/exchange-EUR")
def get_euro_exchange():
    r = requests.get("https://cuantoestaeldolar.pe/")
    r_source_code = r.text
    r_soup = BeautifulSoup(r_source_code, 'html.parser')
    r_elements = r_soup.find_all("div", class_="ValueQuotation_valueContainer__eH4KL")
    exchange_sale = r_elements[6].text
    exchange_buy = r_elements[7].text
    return {
        "sale": float(exchange_sale),
        "buy": float(exchange_buy)
    }

@app.route("/users")
def users():
    return [{
        "id": 1,
        "name": "cristhian"
    }, {
        "id": 2,
        "name": "genaro"
    }]

@app.route("/users/<id>")
def users_by_id(id):
    return {
        "id": id
    }
