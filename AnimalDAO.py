import mysql.connector
from Animal import *
from ConnectionFactory import *
from time import sleep


class AnimalDAO:
    conexao = ConnectionFactory().getConexao()
    def buscaAnimal(self, id):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM ANIMAL WHERE ID_ANIMAL = %s' 
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (id,))
            dados = cursor.fetchone()
            if dados:
                #(self, nome, tipo, raca, genero, idade, desc, status, animalID = None):
                return Animal(nome=dados[1], tipo=dados[2], raca=dados[3],genero=dados[4],idade=dados[5],desc=dados[6], status=dados[7] ,animalID= dados[0] )
            else:
                return None
        except Exception as err:
            print (f"Erro ao buscar animal: {err}")

    def buscaAnimais(self):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM ANIMAL'
            cursor.execute(sql)
            dados = cursor.fetchall()
            animais = []
            for i in dados:
                animal = Animal(nome=dados[1], tipo=dados[2], raca=dados[3],genero=dados[4],idade=dados[5],desc=dados[6], status=dados[7] ,animalID= dados[0] )
                animais.append(animal)
            return animais
        except Exception as err:
            print(f"Erro ao buscar animal: {err}")

    def insereAnimal(self, animal):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            #(nome=dados[1], tipo=dados[2], raca=dados[3],genero=dados[4],idade=dados[5],desc=dados[6], status=dados[7] ,animalID= dados[0] )
            sql = 'INSERT INTO ANIMAL (NOME, TIPO, RACA, GENERO, IDADE, DESCRICAO, STATUSANIMAL) VALUES (%s, %s, %s, %s,%s, %s, %s)'
            cursor.execute(sql, (str(animal.nome), str(animal.tipo), str(animal.raca), int(animal.genero), int(animal.idade), str(animal.desc), str(animal.status)),)
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao inserir animal: {err}")

    def alteraAnimal(self, animal):
        try:
            cursor = self.conexao.cursor()
            sql = 'UPDATE ANIMAL SET NOME = %s, TIPO = %s, GENERO = %s, IDADE = %s, DESCRICAO = %s, STATUSANIMAL = %s WHERE ID_ANIMAL = %s'
            cursor.execute(sql, (animal.nome.upper(), animal.tipo, animal.genero, animal.idade, animal.desc, animal.status, int(animal.animalID),))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao alterar animal: {err}")

    def apagarAnimal(self, animal):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'DELETE FROM ANIMAL WHERE ID_ANIMAL = %s'
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (animal.animalID,))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao apagar animal: {err}")
            

#teste BD Inserir (Funcionando)

'''
animalDAO = AnimalDAO()

#(self, nome, tipo, raca, genero, idade, desc, status, animalID = None):
nome = "May"
tipo = "a"
raca = "b"
genero = 1
idade = 2
desc = "aaaa"
status = "c"

animal = Animal(nome.upper(), tipo, raca, genero, idade, desc, status)
print (animal)
print(animal.tipo)

if animalDAO.insereAnimal(animal):
    print(f"\033[32m\033[1mO Usuario {animal.nome.upper()} foi adicionado com sucesso!\033[0;0m")
'''
