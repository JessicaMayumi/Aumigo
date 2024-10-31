import os
import requests
from UsuarioDAO import *
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from bson.binary import Binary
from ConnectionFactory import *

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

import os

# Caminho relativo
relative_path = 'static/images/person_1.jpg'

absolute_path = os.path.abspath(relative_path)

print("Caminho absoluto:", absolute_path)

if __name__ == "__main__":

    usuarioDAO = UsuarioDAO()
    email_teste = 'test@example.com'
    senha_teste = 'password123'

    usuario = usuarioDAO.buscaUsuario(email_teste, senha_teste)
    
    if usuario:
        print(f"Usuário encontrado: {usuario.nome}")
    else:
        print("Usuário não encontrado ou senha incorreta")




fs = GridFS(db)



def store_image_binary(image_path):
    client = MongoClient("mongodb+srv://AUMIGO:MAY@aumigo.ziyhr.mongodb.net/?authMechanism=SCRAM-SHA-1&ssl=true")
    db = client["AUMIGO"]

    with open(image_path, 'rb') as image_file:
        image_data = Binary(image_file.read())

    db.Usuarios.insert_one({
        '_id': "66e2f6cb960573d1adf9aaaa",
        'filename': os.path.basename(image_path),
        'image': image_data
    })

store_image_binary('static/images/person_1.jpg')

def retrieve_image_binary(user_id, filename, output_path):
    client = MongoClient("mongodb+srv://AUMIGO:MAY@aumigo.ziyhr.mongodb.net/?authMechanism=SCRAM-SHA-1&ssl=true")
    db = client["AUMIGO"]

    # Recupera a imagem do banco de dados
    image_data = db.images.find_one({'user_id': user_id, 'filename': filename})

    if image_data:
        with open(output_path, 'wb') as image_file:
            image_file.write(image_data['image'])
        print(f"Imagem salva em: {output_path}")
    else:
        print("Imagem não encontrada.")

# Exemplo de uso
retrieve_image_binary('66e2f6cb960573d1adf9aaaa', 'image.jpg', '/path/to/output/image.jpg')
