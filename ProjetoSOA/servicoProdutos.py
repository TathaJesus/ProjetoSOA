from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

produtos = [
    {"id": 1, "nome": "Notebook", "preco": 2500},
    {"id": 2, "nome": "Mouse", "preco": 100},
    {"id": 3, "nome": "Teclado", "preco": 200},
]

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos)

@app.route("/produtos/<int:id>", methods=["GET"])
def detalhes_produto(id):
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)
