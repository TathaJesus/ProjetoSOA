from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)


URL_PRODUTOS = "http://localhost:5001"
URL_CARRINHO = "http://localhost:5002"
URL_PAGAMENTO = "http://localhost:5003"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/produtos", methods=["GET"])
def listar_produtos():
    resp = requests.get(f"{URL_PRODUTOS}/produtos")
    return jsonify(resp.json()), resp.status_code


@app.route("/api/carrinho", methods=["GET", "POST", "DELETE"])
def gerenciar_carrinho():
    if request.method == "GET":
        resp = requests.get(f"{URL_CARRINHO}/carrinho")
    elif request.method == "POST":
        resp = requests.post(f"{URL_CARRINHO}/carrinho", json=request.json)
    else:  # DELETE
        item_id = request.args.get("id")
        resp = requests.delete(f"{URL_CARRINHO}/carrinho/{item_id}")
    return jsonify(resp.json()), resp.status_code


@app.route("/api/comprar", methods=["POST"])
def realizar_pagamento():
    # 1. Obter carrinho
    carrinho = requests.get(f"{URL_CARRINHO}/carrinho").json()
    # 2. Enviar para o serviço de pagamento
    resp = requests.post(f"{URL_PAGAMENTO}/pagamento", json=carrinho)
    # 3. Se pagamento ok, limpar carrinho
    if resp.status_code == 200:
        requests.delete(f"{URL_CARRINHO}/carrinho/limpar")
    return jsonify(resp.json()), resp.status_code


if __name__ == "__main__":
    app.run(port=5000, debug=True)
