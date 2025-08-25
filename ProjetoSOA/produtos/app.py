from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # habilita CORS (caso você use frontend depois)

# Banco de dados fake (lista de dicionários)
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00},
    {"id": 2, "nome": "Mouse Gamer", "preco": 150.00},
    {"id": 3, "nome": "Teclado Mecânico", "preco": 300.00}
]

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos)

@app.route("/produtos/<int:produto_id>", methods=["GET"])
def obter_produto(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)
