import os
import requests

# URL do endpoint da API do MongoDB Data API
url = 'https://sa-east-1.aws.data.mongodb-api.com/app/data-appojul/endpoint/data/v1/action/findOne'

# Substitua <API_KEY> pela sua chave de API real
api_key = 'vWz2GhWRTlcMS3yRF5zuWkqbKokTF6TgiLWxLHgh2ybbZXmKAQSCJZNVY6D7i4Ut'

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

# Corpo da requisição
data = {
    "collection": "Usuarios",      # Nome da coleção no MongoDB
    "database": "AUMIGO",          # Nome do banco de dados
    "dataSource": "AUMIGO",        # Nome da fonte de dados
    "projection": {"_id": 1, "nome": 1, "email": 2}  # Ajuste a projeção para incluir campos desejados
}

# Fazer a requisição POST
response = requests.post(url, headers=headers, json=data)

# Verificar a resposta
if response.status_code == 200:
    # Imprimir a resposta JSON de forma legível
    response_data = response.json()
    print("Dados do Objeto Retornado:")
    print(response_data)
else:
    print("Erro:", response.status_code, response.json())
