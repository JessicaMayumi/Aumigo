from Animal import *
from ConnectionFactory import *
from time import sleep
from bson.objectid import ObjectId


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalDAO:
    def __init__(self):
        # Conectar ao MongoDB
        self.collection = db["Animais"]

    def buscaAnimal(self, nome):
        try:
            query = {"nome": nome}
            dados = self.collection.find_one(query)
            if dados:
                return Animal(
                    nome=dados.get("nome"),
                    tipo=dados.get("tipo"),
                    raca=dados.get("raca"),
                    genero=dados.get("genero"),
                    nasc=dados.get("nasc"),
                    desc=dados.get("desc"),
                    status=dados.get("status"),
                    animalID=str(dados.get("_id"))
                )
            else:
                return None
        except Exception as err:
            print(f"Erro ao buscar animal: {err}")

    def buscaAnimais(self):
        try:
            dados = self.collection.find()
            animais = []
            for dado in dados:
                animal = Animal(
                    nome=dados.get("nome"),
                    tipo=dados.get("tipo"),
                    raca=dados.get("raca"),
                    genero=dados.get("genero"),
                    nasc=dados.get("nasc"),
                    desc=dados.get("desc"),
                    status=dados.get("status"),
                    animalID=str(dados.get("_id"))
                )
                animais.append(animal)
            return animais
        except Exception as err:
            print(f"Erro ao buscar animais: {err}")

    def insereAnimal(self, animal):
        try:
            dados = {
                "nome": animal.nome,
                "tipo": animal.tipo,
                "raca": animal.raca,
                "genero": animal.genero,
                "nasc": animal.nasc,
                "desc": animal.desc,
                "status": animal.status
            }
            result = self.collection.insert_one(dados)
            return result.inserted_id is not None
        except Exception as err:
            print(f"Erro ao inserir animal: {err}")

    def alteraAnimal(self, animal):
        try:
            query = {"_id": ObjectId(animal.animalID)}
            novos_dados = {
                "$set": {
                    "nome": animal.nome,
                    "tipo": animal.tipo,
                    "raca": animal.raca,
                    "genero": animal.genero,
                    "nasc": animal.nasc,
                    "desc": animal.desc,
                    "status": animal.status
                }
            }
            result = self.collection.update_one(query, novos_dados)
            return result.modified_count > 0
        except Exception as err:
            print(f"Erro ao alterar animal: {err}")

    def apagarAnimal(self, animal):
        try:
            query = {"animalID": animal.animalID}
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as err:
            print(f"Erro ao apagar usanimal: {err}")

# Exemplo de uso

animalDAO = AnimalDAO()

print(animalDAO.buscaAnimais())
for a in animalDAO.buscaAnimais():
    print(a.nome)
    print(a.senha)
