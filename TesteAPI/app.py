from flask import Flask, request, render_template
import bson
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection  
from pymongo.database import Database

load_dotenv()
connection_string: str = os.environ.get("CONNECTION_STRING")
mongo_client: MongoClient = MongoClient(connection_string)

database: Database = mongo_client.get_database("AUMIGO")
collection: Collection = database.get_collection("Users")

'''user = { 
    "nome" : "May",
    "password" : "123",
    "email" : "may@gmail.com"
}

collection.insert_one(user)
'''
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#Criar e Ler

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        #Criar
        nome : str = request.json["nome"]
        password : str = request.json["password"]
        email: str = request.json["email"]

        #inserir
        collection.insert_one({"nome" : nome,
                               "password" : password,
                               "email" : email})

        return f"O user {nome} foi criado! Senha: {password} e Email: {email}"    

    elif request.method == "GET":
        #LER
        aumigo = list(collection.find())
        usuarios = []

        for nomes in aumigo:
            nome = nomes["nome"]
            password = nomes["password"]
            email = nomes ["email"]
            usuario = {
                "nome" : nome,
                "password" : password,
                "email" : email
            }

            usuarios.insert(0, usuario)

        return usuarios

#UPDATE
@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id: str):
    novoNome: str = request.json["nome"]
    novaSenha: str = request.json["password"]    
    novoEmail: str = request.json["email"]
    collection.update_one({"_id" : bson.ObjectId(user_id)}, {"$set" : {"nome" : novoNome, "password" : novaSenha, "email" : novoEmail} })

    return f"UPDATE: o nome do usuario foi atualizado para {novoNome}, senha: {novaSenha}, email: {novoEmail}"


#DELETAR

@app.route("/users/<string:user_id>", methods=["DELETE"])
def revomer_user(user_id: str):
    collection.delete_one({"_id" : bson.ObjectId(user_id)})

    return f"DELETADO: O usuario (id = {user_id}) foi removido"

""""animal = [
    {
        "id" : 1,
        "nome" : "pompom",
        "tipo": "gato"
    }, 
    {
        "id" : 2,
        "nome" : "rabito",
        "tipo": "coelho"
    }, 
    {
        "id" : 3,
        "nome" : "lua",
        "tipo": "cachorro"
    }, 
]

@app.route("/animal")
def obter_animais():
    return jsonify(animal)"""