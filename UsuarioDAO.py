from Usuario import *
from ConnectionFactory import *
from time import sleep
from bson.objectid import ObjectId


from pymongo import MongoClient
from bson.objectid import ObjectId

class UsuarioDAO:
    def __init__(self):
        # Conectar ao MongoDB
        self.collection = db["Usuarios"]

    def buscaUsuario(self, email, senha):
        try:
            query = {"email": email, "senha": senha}
            dados = self.collection.find_one(query)
            if dados:
                return Usuario(
                    nome=dados.get("nome"),
                    email=dados.get("email"),
                    senha=dados.get("senha"),
                    verificarUser=dados.get("verificarUser"),
                    usuarioID=dados.get("_id")
                )
            else:
                return None
        except Exception as err:
            print(f"Erro ao buscar usuário: {err}")

    def buscaUsuarioPorEmail(self, email):
        try:
            query = {"email": email}
            dados = self.collection.find_one(query)
            if dados:
                return Usuario(
                    nome=dados.get("nome"),
                    email=dados.get("email"),
                    senha=dados.get("senha"),
                    verificarUser=dados.get("verificarUser"),
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
                    usuarioID=str(dado.get("_id"))
                )
                usuarios.append(usuario)
            return usuarios
        except Exception as err:
            print(f"Erro ao buscar usuários: {err}")

    def insereUsuario(self, usuario):
        try:
            dados = {
                "nome": usuario.nome,
                "email": usuario.email,
                "senha": usuario.senha,
                "verificarUser": usuario.verificarUser
            }
            result = self.collection.insert_one(dados)
            return result.inserted_id is not None
        except Exception as err:
            print(f"Erro ao inserir usuário: {err}")

    def alteraUsuario(self, usuario):
        try:
            query = {"_id": ObjectId(usuario.usuarioID)}
            novos_dados = {
                "$set": {
                    "nome": usuario.nome.upper(),
                    "email": usuario.email,
                    "senha": usuario.senha,
                    "verificarUser": usuario.verificarUser
                }
            }
            result = self.collection.update_one(query, novos_dados)
            return result.modified_count > 0
        except Exception as err:
            print(f"Erro ao alterar usuário: {err}")

    def apagarUsuario(self, usuario):
        try:
            query = {"email": usuario.email}
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as err:
            print(f"Erro ao apagar usuário: {err}")

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

print(usuarioDAO.buscaUsuarios())
for user in usuarioDAO.buscaUsuarios():
    print(user.email)
    print(user.senha)
