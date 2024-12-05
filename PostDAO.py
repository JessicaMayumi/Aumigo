from Post import *
from UsuarioDAO import UsuarioDAO
from AnimalDAO import *
from ConnectionFactory import db
import gridfs
from pymongo import MongoClient
import datetime
from bson import ObjectId

class PostDAO:
    def __init__(self):
        self.collection = db["Posts"]
        self.collection_users = db["Usuarios"]

    def adicionaPost(self, post, email):
        try:
            dados = {
                "titulo": post.titulo,
                "status": post.status,
                "visibilidade": post.visibilidade,
                "conteudo": post.conteudo,
                "dataCriacao": post.dataCriacao,
                "autor": post.autor
            }
            print("\033[31mDados a serem inseridos:\033[0;0m", dados)

            result = self.collection.insert_one(dados)
            postId = result.inserted_id
            print("\033[31mID do post inserido:\033[0;0m", postId)

            if postId:
                usuarioDAO = UsuarioDAO()
                usuario = usuarioDAO.buscaUsuarioPorEmail(email)
                print("\033[31mUsuário encontrado:\033[0;0m", usuario)
                
                if usuario:
                    query = {"_id": ObjectId(usuario.usuarioID)}
                    novos_dados = {
                        "$push": {
                            "posts": {
                                "$each": [str(postId)],
                                "$position": 0 
                            }
                        }
                    }
                    print("\033[31mPosts atualizados:\033[0;0m", usuario.posts)
                    result = usuarioDAO.collection.update_one(query, novos_dados)
                    if result.modified_count > 0:
                        print(f"\033[31mPost {postId} adicionado ao usuário {email}.\033[0;0m")
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
            print(f"Erro ao inserir Post: {err}")
            return False


    def buscaPostsPorUsuario(self, email):
        try:
            usuarioDAO = UsuarioDAO()

            usuario = usuarioDAO.buscaUsuarioPorEmail(email)
            print(f"\033[36mUsuário encontrado: {usuario}\033[0m")
            
            if usuario:
                print(f"\033[36mUsuário encontrado 2: {usuario}\033[0m")
                
                if usuario.posts:
                    print(f"\033[36mPosts encontrados para o usuário: {usuario.posts}\033[0m")

                    postsIDs = usuario.posts
                    
                    print(f"\033[36m{postsIDs}\033[0m") 
                    return self.buscaPostsPorIDs(postsIDs) 
                else:
                    print("Usuário não tem posts associados.")
                    return []
            else:
                print("Usuário não encontrado.")
                return []
        except Exception as err:
            print(f"Erro ao buscar posts do usuário: {err}")
            return []

    def buscaPosts(self):
        posts = []
        try:
            dados_posts = self.collection.find() 
            for post_data in dados_posts:
                post = Post(
                    titulo=post_data.get("titulo"),
                    conteudo=post_data.get("conteudo"),
                    status=post_data.get("status"),
                    visibilidade=post_data.get("visibilidade"),
                    dataCriacao=post_data.get("dataCriacao"),
                    autor=post_data.get("autor"),
                    postID=str(post_data.get("_id"))  
                )
                posts.append(post)
            return posts
        except Exception as err:
            print(f"Erro ao buscar posts: {err}")
            return []
        

    def buscaPost(self, id):    
        try:
            post = self.collection.find_one({"_id": ObjectId(id)})
            if post:
                return post
            else:
                print(f"Post com ID {id} não encontrado.")
                return None
        except Exception as err:
            print(f"Erro ao buscar post com id: {err}")
            return None

    def editarPost(self, id):
        try:
            post = self.collection.find_one({"_id": ObjectId(id)})
            query = {"_id": ObjectId(post.postID)}
            novos_dados = {
                "$set": {
                    "_id": id,	
                    "titulo": post.titulo,
                    "status": post.status,
                    "visibilidade": post.visibilidade,
                    "conteudo": post.conteudo,
                    "dataCriacao": post.dataCriacao,
                    "autor": post.autor
                }
            }
            print("\033[31mDados a serem inseridos:\033[0;0m", novos_dados)

            result = self.collection.update_one(query, novos_dados)
            if result.modified_count > 0:
                print(f"\033[31mPost {id} editado com sucesso.\033[0;0m")
                return True
            else:
                print(f"Erro ao editar o post {id}.")
                return False
        except Exception as err:
            print(f"Erro ao editar Post: {err}")
            return False
    
    def buscaPostsPorIDs(self, postsIDs):
        posts = []
        try:
            print(postsIDs)
            object_id = ObjectId(str(postsIDs[0]))  # Converte para ObjectId
            post = self.collection.find_one({"_id": object_id})
            
            if post:
                print(f"Post encontrado: {post}")
                posts.append(post)
            else:
                print(f"Post com ID {postsIDs} não encontrado.")
            print("\033[31mPosts encontrados:\033[0;0m", posts)
            return posts
        except Exception as err:
            print(f"Erro ao buscar posts lista: {err}")
            return []

    def apagarPost(self, post_id):
        try:
            post_id_object = ObjectId(post_id)

            query = {"_id": post_id_object}
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                usuario_query = {"posts": {"$in": [ObjectId(post_id), post_id]}}
                usuario = self.collection_users.find_one(usuario_query)

                if usuario:

                    if "posts" in usuario:
                        lista_posts_objectid = [ObjectId(p) if isinstance(p, str) else p for p in usuario['posts']]

                        if post_id_object in lista_posts_objectid:
                            usuario['posts'].remove(str(post_id_object))
                            update_result = self.collection_users.update_one(
                                {"_id": usuario["_id"]},
                                {"$set": {"posts": usuario["posts"]}}
                            )

                            print(f"Resultado da atualização: {update_result.modified_count} documentos modificados.")

                            usuario_atualizado = self.collection_users.find_one({"_id": usuario["_id"]})
                            print(f"Dados do usuário após atualização: {usuario_atualizado}")

                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return True

        except Exception as err:
            return False