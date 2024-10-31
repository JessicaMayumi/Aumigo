from Animal import *
from ConnectionFactory import *
from time import sleep
from UsuarioDAO import *
from Usuario import *

from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalDAO:
    def __init__(self):
        # Conectar ao MongoDB
        self.collection = db["Animais"]

    def buscaAnimal(self, animalID):
        try:
            query = {"animalID": animalID}
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
                    foto = dados.get("foto"),
                    animalID=str(dados.get("_id"))
                )
            else:
                return None
        except Exception as err:
            print(f"Erro ao buscar animal: {err}")

    def buscaAnimais(self, parametro):
        try:
            # Converte cada ID da lista para ObjectId *NAO ENTENDI*
            object_ids = []
            for animal_id in parametro:
                object_ids.append(ObjectId(animal_id))
            
            # Faz a busca no banco de dados usando os ObjectId *NAO ENTENDI*
            query = {"_id": {"$in": object_ids}}
            dados = self.collection.find(query)
            animais = []
            for dado in dados:
                animal = Animal(
                    nome=dado.get("nome"),
                    tipo=dado.get("tipo"),
                    raca=dado.get("raca"),
                    genero=dado.get("genero"),
                    nasc=dado.get("nasc"),
                    desc=dado.get("desc"),
                    status=dado.get("status"),
                    foto = dado.get("foto"),
                    animalID=str(dado.get("_id"))
                )
                animais.append(animal)
            return animais
        except Exception as err:
            print(f"Erro ao buscar animais: {err}")

    def buscaAnimaisPorUsuario(self, email):    
        try:
            usuario = usuarioDAO.buscaUsuarioPorEmail(email)
            print("Usuário encontrado:", usuario)

            if usuario:
                print("Animais do usuário:", usuario.animais)  # Para verificar a lista de animais
                if usuario.animais:  # Verifica se a lista de animais não está vazia
                    animalIDs = usuario.animais
                    print(f"IDs dos animais: {animalIDs}")
                    return self.buscaAnimais(animalIDs)
                else:
                    print(f"Usuário não tem animais associados.")
                    return []
            else:
                print("Usuário não encontrado.")
                return []
        except Exception as err:
            print(f"Erro ao buscar animais do usuário: {err}")
            return []
        
    def adicionaAnimalAoUsuario(self, usuario_email, animal_id):
        try:
            result = self.collection.update_one(
                {"email": usuario_email},
                {"$addToSet": {"animais": animal_id}}
            )
            
            if result.modified_count > 0:
                print(f"Animal {animal_id} adicionado ao usuário {usuario_email}.")
            else:
                print(f"Falha ao adicionar animal ao usuário {usuario_email}.")
        except Exception as err:
            print(f"Erro ao associar animal ao usuário: {err}")

    def insereAnimal(self, animal, email):
        try:
            # Inserindo o animal na coleção de animais
            dados = {
                "nome": animal.nome,
                "tipo": animal.tipo,
                "raca": animal.raca,
                "genero": animal.genero,
                "nasc": animal.nasc,
                "desc": animal.desc,
                "status": animal.status,
                "foto" : animal.foto
            }
            result = self.collection.insert_one(dados)
            animal_id = result.inserted_id
            
            if animal_id:
                usuarioDAO = UsuarioDAO()
                usuario = usuarioDAO.buscaUsuarioPorEmail(email)
                
                if usuario:
                    usuario.animais.append(str(animal_id))
                    
                    if usuarioDAO.alteraUsuario(usuario):
                        print(f"Animal {animal_id} adicionado ao usuário {email}.")
                        return True
                    else:
                        print(f"Erro ao atualizar o usuário {email}.")
                        return False
                else:
                    print(f"Usuário {email} não encontrado.")
                    return False
            else:
                return False
        except Exception as err:
            print(f"Erro ao inserir animal: {err}")
            return False

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
                    "status": animal.status,
                    "foto" : animal.foto
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

'''animalDAO = AnimalDAO()

print(animalDAO.buscaAnimais())
for a in animalDAO.buscaAnimais():
    print(a.nome)'''


animalDAO = AnimalDAO()


# Teste
'''novo_animal = Animal("a", "b", "c", "d", "e", "f", "g", foto=None)
if animalDAO.insereAnimal(novo_animal):
    print("foi")'''
'''email = "BBBB@GMAIL.COM"
usuario = usuarioDAO.buscaUsuarioPorEmail(email)
print(f"Usuário encontrado: {usuario}, Animais: {usuario.animais}")'''


'''usuario_test = Usuario("Nome", "email@example.com", "senha123", True, "img.jpg", "Descrição", ["animal1", "animal2"])
print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
print(usuario_test.animais)  # Deve imprimir a lista de animais
#   ESTÁ FUNCIONANDO!
'''