from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/pagamento", methods=["POST"])
def processar_pagamento():
    data = request.get_json()
    total = data.get("total")
    if total and total > 0:
        return jsonify({"status": "sucesso", "mensagem": f"Pagamento de R${total} confirmado!"})
    return jsonify({"status": "falha", "mensagem": "Valor inválido"}), 400

if __name__ == "__main__":
    app.run(port=5003, debug=True)
