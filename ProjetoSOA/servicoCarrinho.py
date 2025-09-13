from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

carrinho = []

@app.route("/carrinho", methods=["GET"])
def listar_carrinho():
    return jsonify(carrinho)

@app.route("/carrinho", methods=["POST"])
def adicionar_carrinho():
    data = request.get_json()
    produto_id = data.get("id")

    resp = requests.get(f"http://localhost:5001/produtos/{produto_id}")
    if resp.status_code == 200:
        produto = resp.json()
        carrinho.append(produto)
        return jsonify({"mensagem": "Produto adicionado", "carrinho": carrinho})
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/carrinho", methods=["DELETE"])
def limpar_carrinho():
    carrinho.clear()
    return jsonify({"mensagem": "Carrinho limpo!"})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
