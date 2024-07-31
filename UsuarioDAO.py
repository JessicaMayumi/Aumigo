import mysql.connector
from Usuario import *
from ConnectionFactory import *
from time import sleep


class UsuarioDAO:
    conexao = ConnectionFactory().getConexao()
    def buscaUsuario(self, email):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM USUARIO WHERE EMAIL = %s' 
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (email,))
            dados = cursor.fetchone()
            if dados:
                #(self, nome, email, senha, verificarUser, usuarioID = None)
                return Usuario(nome=dados[1], email=dados[2], senha=dados[3],verificarUser=dados[4],usuarioID= dados[0]  )
            else:
                return None
        except Exception as err:
            print (f"Erro ao buscar usuário: {err}")

    def buscaUsuarios(self):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM USUARIO'
            cursor.execute(sql)
            dados = cursor.fetchall()
            usuarios = []
            for i in dados:
                usuario = Usuario(nome=dados[1], email=dados[2], senha=dados[3],verificarUser=dados[4],usuarioID= dados[0]  )
                usuarios.append(usuario)
            return usuarios
        except Exception as err:
            print(f"Erro ao buscar usuário: {err}")

    def insereUsuario(self, usuario):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            #(self, nome, email, senha, verificarUser, usuarioID = None)
            sql = 'INSERT INTO USUARIO (NOME, EMAIL, SENHA, VERIFICARUSER) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (str(usuario.nome), str(usuario.email), str(usuario.senha), str(usuario.verificarUser)),)
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao inserir usuário: {err}")

    def alteraUsuario(self, usuario):
        try:
            cursor = self.conexao.cursor()
            sql = 'UPDATE USUARIO SET NOME = %s, EMAIL = %s,  SENHA = %s, VERIFICARUSER = %s WHERE ID_USUARIO = %s'
            cursor.execute(sql, (usuario.nome.upper(), usuario.email, usuario.senha, usuario.verificarUser, int(usuario.usuarioID),))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao alterar usuario: {err}")

    def apagarUsuario(self, usuario):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'DELETE FROM USUARIO WHERE EMAIL = %s'
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (usuario.email,))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao apagar usuário: {err}")
            
usuarioDAO = UsuarioDAO()
#teste BD 

'''



nome = "Lia"
email = "uwu.jessyca@gmail.com"
senha = "145"
verificarUser = "N"
usuario = Usuario(nome.upper(), email.upper(), senha, verificarUser)

if usuarioDAO.insereUsuario(usuario): #Inserir Funcionando
    print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")

#if usuarioDAO.apagarUsuario(usuario): #Apagar Funcionando
#    print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi apagado com sucesso!\033[0;0m")

#if usuarioDAO.alteraUsuario(usuario):  #Alterar ERRO
#    print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")

#if usuarioDAO.buscaUsuario(usuario.email):  #Listar Usuário ERRO
#    print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")
 
#for item in usuarioDAO.buscaUsuarios(): #Listar Usuários ERRO
#    print(item)

'''
