from pymongo import MongoClient
import gridfs

client = MongoClient("mongodb+srv://AUMIGO:MAY@aumigo.ziyhr.mongodb.net/?authMechanism=SCRAM-SHA-1&ssl=true")

# Acessando o banco de dados
db = client["AUMIGO"]

# Acessando uma coleção
#collection = db["Usuarios"]

'''
# Exemplo de inserção de documento na coleção
collection.insert_one({"name": "John", "age": 30})

# Exemplo de leitura de documentos da coleção
for document in collection.find():
    print(document)
'''