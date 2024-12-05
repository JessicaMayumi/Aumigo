from PostDAO import PostDAO
from ConnectionFactory import *
from time import sleep
from UsuarioDAO import UsuarioDAO
from Usuario import *
from Animal import *

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import ObjectId

class AnimalDAO:
    def __init__(self):
        self.collection = db["Animais"]
        self.collection_users = db["Usuarios"]
        self.fs = gridfs.GridFS(db) 

    def buscaAnimal(self, animalID):
        try:
            if isinstance(animalID, str):
                animalID = ObjectId(animalID)
            
            query = {"_id": animalID}
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
            object_ids = []
            for animal_id in parametro:
                object_ids.append(ObjectId(animal_id))
            
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
            usuarioDAO = UsuarioDAO()
            usuario = usuarioDAO.buscaUsuarioPorEmail(email)
            print("Usuário encontrado:", usuario)

            if usuario:
                print("Animais do usuário:", usuario.animais)  
                if usuario.animais:  
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
           
            dados = {
                "nome": animal.nome,
                "tipo": animal.tipo,
                "raca": animal.raca,
                "genero": animal.genero,
                "nasc": animal.nasc,
                "desc": animal.desc,
                "status": animal.status,
                "foto": [self.fs.put(f.read(), filename=f.filename) for f in animal.foto] if animal.foto else []
                # "dataCriacao": datetime.datetime.utcnow()
            }
            print("\033[31mDados do animal a serem inseridos:\033[0;0m", dados)

            result = self.collection.insert_one(dados)
            animalId = result.inserted_id
            print("\033[31mID do animal inserido:\033[0;0m", animalId)

            if animalId:
                usuarioDAO = UsuarioDAO()
                usuario = usuarioDAO.buscaUsuarioPorEmail(email)
                print("\033[31mUsuário encontrado:\033[0;0m", usuario)

                if usuario:
                    query = {"_id": ObjectId(usuario.usuarioID)}
                    novos_dados = {
                        "$push": {
                            "animais": {
                                "$each": [str(animalId)],
                                "$position": 0
                            }
                        }
                    }
                    print("\033[31mAnimais atualizados:\033[0;0m", usuario.animais)

                    result = usuarioDAO.collection.update_one(query, novos_dados)
                    if result.modified_count > 0:
                        print(f"\033[32mAnimal {animalId} adicionado ao usuário {email}.\033[0;0m")
                        return True
                    else:
                        print(f"\033[31mErro ao atualizar o usuário {email}.\033[0;0m")
                        return False
                else:
                    print(f"\033[31mUsuário {email} não encontrado.\033[0;0m")
                    return False
            else:
                return False
        except Exception as err:
            print(f"\033[31mErro ao inserir animal: {err}\033[0;0m")
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



    def apagarAnimal(self, animal_id):
        try:
            animal_id_object = ObjectId(animal_id)

            print(f"Removendo animal com id {animal_id_object} da coleção de animais.")
            query = {"_id": animal_id_object}
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                print(f"Animal {animal_id} removido do banco de dados.")
            else:
                print(f"Falha ao remover o animal {animal_id}.")

            usuario_query = {"animais": {"$in": [ObjectId(animal_id), animal_id]}}
            usuario = self.collection_users.find_one(usuario_query)
            print(f"Consulta para buscar usuário com animal {animal_id}: {usuario_query}")
            
            if usuario:
                print(f"Dados do usuário encontrado: {usuario}")

                if "animais" in usuario:
                    print(f"Lista de animais do usuário antes da remoção: {usuario['animais']}")

                    lista_animais_objectid = [ObjectId(a) if isinstance(a, str) else a for a in usuario['animais']]
                    print(f"Lista de animais após conversão para ObjectId: {lista_animais_objectid}")

                    if animal_id_object in lista_animais_objectid:
                        usuario['animais'].remove(str(animal_id_object)) 
                        
                        print(f"Animal {animal_id_object} removido da lista de animais.")

                        update_result = self.collection_users.update_one(
                            {"_id": usuario["_id"]},
                            {"$set": {"animais": usuario["animais"]}}
                        )
                        print(f"Resultado da atualização: {update_result.modified_count} documentos modificados.")

                        usuario_atualizado = self.collection_users.find_one({"_id": usuario["_id"]})
                        print(f"Dados do usuário após atualização: {usuario_atualizado}")

                        return True
                    else:
                        print(f"Animal {animal_id_object} não encontrado na lista de animais do usuário.")
                        return False
                else:
                    print("A chave 'animais' não encontrada no usuário.")
                    return False
            else:
                print(f"Animal {animal_id} removido, mas não encontrado em nenhum usuário.")
                return True

        except Exception as err:
            print(f"Erro ao apagar animal: {err}")
            return False







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

'''    def apagarAnimal(self, animal_id):
        try:
            # Remover o animal da coleção de animais usando animal_id
            query = {"_id": ObjectId(animal_id)}  # Convertendo animal_id para ObjectId
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                # Buscar o usuário que possui este animal
                usuario_query = {"animais": animal_id}  # Usando diretamente animal_id
                usuario = self.collection_users.find_one(usuario_query)
                animal_index = usuario["animais"].index(animal_id)

                if usuario:
                    # Atualizar a lista de animais do usuário
                    usuario_obj = Usuario(
                        nome=usuario["nome"],
                        email=usuario["email"],
                        senha=usuario["senha"],
                        verificarUser=usuario["verificarUser"],
                        imgPerfil=usuario.get("imgPerfil"),
                        desc=usuario.get("desc", ""),
                        animais=usuario["animais"].remove(animal_index)  # Removendo o animal pelo ID
                    )

                    if self.alteraUsuario(usuario_obj):
                        print(f"Animal {animal_id} removido do banco e atualizado no usuário {usuario_obj.usuarioID}.")
                        return True
                    else:
                        print(f"Erro ao atualizar o usuário {usuario_obj.usuarioID} ao remover o animal {animal_id}.")
                        return False
                else:
                    print(f"Animal {animal_id} removido, mas não encontrado em nenhum usuário.")
                    return True
            else:
                print("Nenhum animal encontrado para remover.")
                return False

        except Exception as err:
            print(f"Erro ao apagar animal: {err}")
            return False'''


