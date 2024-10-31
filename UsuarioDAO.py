from Usuario import *
from ConnectionFactory import *
from time import sleep
from bson.objectid import ObjectId
from bson.binary import Binary

from pymongo import MongoClient
from bson.objectid import ObjectId

class UsuarioDAO:
    def __init__(self):
        # Conectar ao MongoDB
        self.collection = db["Usuarios"]
        self.fs = gridfs.GridFS(db)

    def buscaUsuario(self, email, senha):
        try:
            query = {"email": email.upper(), "senha": senha}
            dados = self.collection.find_one(query)
            if dados:
                return Usuario(
                    nome=dados.get("nome"),
                    email=dados.get("email"),
                    senha=dados.get("senha"),
                    verificarUser=dados.get("verificarUser"),
                    imgPerfil=dados.get("imgPerfil"),
                    desc=dados.get("desc"),
                    animais=dados.get("animais", []),
                    usuarioID=str(dados.get("_id"))
                )
            else:
                print("Usuário não encontrado.")
                return None
        except Exception as err:
            print(f"Erro ao buscar usuário: {err}")

    def buscaUsuarioPorEmail(self, email):
        try:
            query = {"email": email.upper()}
            dados = self.collection.find_one(query)
            if dados:
                animais=dados.get("animais", [])
                print("Lista de animais:", animais)

                return Usuario(
                    nome=dados.get("nome"),
                    email=dados.get("email"),
                    senha=dados.get("senha"),
                    verificarUser=dados.get("verificarUser"),
                    imgPerfil=dados.get("imgPerfil"),
                    desc=dados.get("desc"),
                    animais=animais,
                    usuarioID=dados.get("_id")
                )
            else:
                return None
        except Exception as err:
            print(f"Erro ao buscar usuário: {err}")

    def buscaUsuarios(self):
        try:
            dados = self.collection.find()
            usuarios = []
            for dado in dados:
                usuario = Usuario(
                    nome=dado.get("nome"),
                    email=dado.get("email"),
                    senha=dado.get("senha"),
                    verificarUser=dado.get("verificarUser"),
                    imgPerfil=dado.get("imgPerfil"),
                    desc=dado.get("desc"),
                    animais=dado.get("animais", []),
                    usuarioID=str(dado.get("_id"))
                )
                usuarios.append(usuario)
            return usuarios
        except Exception as err:
            print(f"Erro ao buscar usuários: {err}")
            return [] 


    def insereUsuario(self, usuario):
        try:
            # Carrega a imagem padrão em bytes e armazena no GridFS, se não houver imagem personalizada
            img_id = None
            with open("static/images/person-1.jpg", 'rb') as f:  # caminho para a imagem padrão
                img_data = f.read()
                img_id = self.fs.put(img_data, filename="person-1.jpg")

            dados = {
                "nome": usuario.nome,
                "email": usuario.email,
                "senha": usuario.senha,
                "verificarUser": usuario.verificarUser,
                "imgPerfil": img_id,  # Armazena o ID do GridFS em vez do caminho
                "desc": usuario.desc,
                "animais": usuario.animais
            }
            result = self.collection.insert_one(dados)
            return result.inserted_id is not None
        except Exception as err:
            print(f"Erro ao inserir usuário: {err}")
            return False


    def alteraUsuario(self, usuario):
        try:
            # Define a consulta pelo ID do usuário
            query = {"_id": ObjectId(usuario.usuarioID)}
            print(f"\nIniciando atualização do usuário com ID: {usuario.usuarioID}")

            # Obtém o documento atual do usuário
            current_user = self.collection.find_one(query)
            if not current_user:
                print(f"Erro: Usuário com ID {usuario.usuarioID} não encontrado no banco de dados.")
                return False

            print(f"Dados atuais do usuário: {current_user}")

            # Define a nova imagem de perfil
            img_id_str = usuario.imgPerfil if usuario.imgPerfil else current_user.get('imgPerfil')
            if img_id_str:
                print("Usando nova imagem de perfil fornecida." if usuario.imgPerfil else "Mantendo a imagem de perfil existente.")
            else:
                print("Nenhuma imagem de perfil fornecida.")

            # Dados a serem atualizados
            novos_dados = {
                "$set": {
                    "nome": usuario.nome.lower(),
                    "email": usuario.email,
                    "senha": usuario.senha,
                    "verificarUser": usuario.verificarUser,
                    "imgPerfil": img_id_str,
                    "desc": usuario.desc,
                    "animais": usuario.animais
                }
            }
            print(f"Novos dados para atualização: {novos_dados}")

            # Realiza a atualização no banco de dados
            result = self.collection.update_one(query, novos_dados)
            print(f"Documentos modificados: {result.modified_count}")

            # Verifica o documento atualizado para garantir que a imagem foi alterada
            updated_user = self.collection.find_one(query)
            print(f"\nDocumento atualizado: {updated_user}")

            if result.modified_count > 0:
                print("Atualização realizada com sucesso.")
            else:
                print("Nenhuma modificação foi realizada no banco de dados.")

            return result.modified_count > 0
        except Exception as err:
            print(f"Erro ao alterar usuário: {err}")
            return False


    def apagarUsuario(self, usuario):
        try:
            query = {"email": usuario.email}
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as err:
            print(f"Erro ao apagar usuário: {err}")

    def adicionarAnimalAoUsuario(self, usuarioID, animalID):
        try:
            query = {"_id": ObjectId(usuarioID)}
            novo_animal = {"$push": {"animais": animalID}}
            result = self.collection.update_one(query, novo_animal)
            return result.modified_count > 0
        except Exception as err:
            print(f"Erro ao adicionar animal ao usuário: {err}")
            return False



# Exemplo de uso

usuarioDAO = UsuarioDAO()

'''
# Teste
novo_usuario = Usuario(nome="May", email="may@example.com", senha="123456", verificarUser=True)
usuarioDAO.insereUsuario(novo_usuario)



usuario = usuarioDAO.buscaUsuario("star@gmail.com".upper(), "123")
if usuario:
    print(f"Usuário encontrado: {usuario.nome}, Tipo: {usuario.verificarUser}")
else:
    print("Usuário não encontrado ou senha incorreta")

'''

"""

print(usuarioDAO.buscaUsuarios())
for user in usuarioDAO.buscaUsuarios():
    print(user.email)
    print(user.senha)

novo_usuario = Usuario(nome="May", email="may@example.com", senha="123456", verificarUser="N", imgPerfil="static/images/person-1.png", desc= "aaaa")
if usuarioDAO.insereUsuario(novo_usuario):
    print("Usuário inserido com sucesso")
"""
usuarios = usuarioDAO.buscaUsuarios()
for user in usuarios:
    print(f"Email: {user.email}, Senha: {user.senha}")

"""usuario = usuarioDAO.buscaUsuario("may@example.com", "123456")
if usuario:
    print(f"Usuário encontrado: {usuario.nome}, Tipo: {usuario.verificarUser}, Img: {usuario.imgPerfil}, Senha: {usuario.senha}")
else:
    print("Usuário não encontrado ou senha incorreta")

usuarioDAO.alteraUsuario(usuario)"""

"""novo_usuario = Usuario(
    nome="May", 
    email="may@example.com", 
    senha="123456", 
    verificarUser="N", 
    imgPerfil="static/images/person-1.png", 
    desc="aaaa"
)

if usuarioDAO.insereUsuario(novo_usuario):
    print("Usuário inserido com sucesso")
else:
    print("Falha ao inserir usuário")"""

email = "BBBB@GMAIL.COM"
senha = "123"

usuario = usuarioDAO.buscaUsuario(email, senha)
if usuario:
    print(f"Usuário encontrado: {usuario.nome}, Tipo: {usuario.verificarUser}, Img: {usuario.imgPerfil}")
else:
    print("Usuário não encontrado ou senha incorreta")

'''

usuarioID = "66e2f6cb960573d1adf9aaaa"
animalID = "66f1859c2ca923f5e745da5e"

if usuarioDAO.adicionarAnimalAoUsuario(usuarioID, animalID):
    print("Animal adicionado ao usuário com sucesso!")
else:
    print("Erro ao adicionar animal ao usuário.")'''


usuario = usuarioDAO.buscaUsuarioPorEmail(email)
if usuario:
    print(f"Usuário encontrado: {usuario.nome}, Tipo: {usuario.verificarUser}, Img: {usuario.imgPerfil}")



"""   def insereUsuario(self, usuario):
        try:
            # Verifica se o usuário enviou uma imagem; se não, usa uma imagem padrão
            if usuario.imgPerfil:
                if isinstance(usuario.imgPerfil, str):
                    with open(usuario.imgPerfil, 'rb') as f:
                        img_data = f.read()
                    img_id = self.fs.put(img_data, filename=usuario.imgPerfil)
                    img_id_str = str(img_id)
                else:
                    img_id_str = None
            else:
                img_id_str = "static/images/person-1.jpg"
            
            dados = {
                "nome": usuario.nome,
                "email": usuario.email,
                "senha": usuario.senha,
                "verificarUser": usuario.verificarUser,
                "imgPerfil": img_id_str,  # Usa a imagem padrão ou a personalizada
                "desc": usuario.desc,
                "animais": usuario.animais
            }
            result = self.collection.insert_one(dados)
            return result.inserted_id is not None
        except Exception as err:
            print(f"Erro ao inserir usuário: {err}")"""

