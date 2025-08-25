import requests

# Consultar todos os produtos
resp = requests.get("http://127.0.0.1:5001/produtos")
print("Lista de produtos:", resp.json())

# Consultar produto específico
resp = requests.get("http://127.0.0.1:5001/produtos/2")
print("Produto ID=2:", resp.json())

# Consultar produto inexistente
resp = requests.get("http://127.0.0.1:5001/produtos/99")
print("Produto ID=99:", resp.json())
