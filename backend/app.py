from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route("/")
def ola_mundo():
    return "Olá mundo"

@app.route("/<string:nome>")
def ola(nome: str):
    return f'Olá {nome}'


with app.test_request_context():
    print(url_for("ola_mundo"))