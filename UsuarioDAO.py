import mysql.connector
from Usuario import *
from ConnectionFactory import *


class FuncionarioDAO:
    conexao = ConnectionFactory().getConexao()


    def buscaUsuario(self, email):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM FUNCIONARIO WHERE CPF = %s' 
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (email,))
            dados = cursor.fetchone()
            if dados:
                return Usuario(nome=dados[1], email=dados[2], senha=dados[3],verificarUser=dados[4],usuarioID= dados[0]  )
            else:
                return None
        except Exception as err:
            print (f"Erro ao buscar funcionário: {err}")

    def buscaFuncionarios(self):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'SELECT * FROM FUNCIONARIO'
            cursor.execute(sql)
            dados = cursor.fetchall()
            funcionarios = []
            for i in dados:
                funcionario = Usuario(nome=i[2], cargo=i[3], salario=i[4],cpf=i[1],dataContratacao = i[5], restauranteID = i[6], funcionarioID = i[0],  )
                funcionarios.append(funcionario)
            return funcionarios
        except Exception as err:
            print(f"Erro ao buscar funcionários: {err}")

    def buscaRestauranteNome(self, nome):
        try:
            cursor = self.conexao.cursor()
            sql = 'SELECT * FROM RESTAURANTE WHERE NOME LIKE %s' 
            cursor.execute(sql, (nome,))
            dados = cursor.fetchone()
            if dados:
                return Funcionario(nome=dados[2], cargo=dados[3], salario=dados[4],cpf=dados[1],dataContratacao = dados[5], restauranteID = dados[6], funcionarioID = dados[0],  )
            else:
                return None
        except Exception as err:
            print (f"Erro ao buscar restaurante: {err}")

    def insereFuncionario(self, funcionario):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'INSERT INTO FUNCIONARIO (CPF, NOME, CARGO, SALARIO, DATA_DE_CONTRATACAO, ID_RESTAURANTE) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (str(funcionario.cpf), str(funcionario.nome), str(funcionario.cargo), float(funcionario.salario), dataSQL(funcionario.dataContratacao), int(funcionario.restauranteID),))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao inserir funcionário: {err}")

    def alteraFuncionario(self, funcionario):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            # sql = 'UPDATE FUNCIONARIO SET NOME = %s, CARGO = %s, SALARIO = %s, DATA_DE_CONTRATACAO = %s, ID_RESTAURANTE = %s WHERE ID_FUNCIONARIO = %s'
            # cursor.execute(sql, (funcionario.nome, funcionario.cargo, float(funcionario.salario), dataSQL(funcionario.dataContratacao), int(funcionario.restauranteID), int(funcionario.funcionarioID)))
            sql = 'UPDATE FUNCIONARIO SET NOME = %s, CARGO = %s, SALARIO = %s WHERE ID_FUNCIONARIO = %s'
            cursor.execute(sql, (funcionario.nome.upper(), funcionario.cargo, funcionario.salario, int(funcionario.funcionarioID),))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao alterar funcionário: {err}")

    def apagarFuncionario(self, funcionario):
        try:
            cursor = self.conexao.cursor()
            ### Necessário usar o SQL em maiusculo pq o UBUNTU é case sensitive e sempre o SQL maisuculo no DAO também
            sql = 'DELETE FROM FUNCIONARIO WHERE CPF = %s'
            ##necessário id, para identificar como tupla senão não lê do banco
            cursor.execute(sql, (funcionario.cpf,))
            self.conexao.commit()
            return True
        except Exception as err:
            print(f"Erro ao apagar funcionário: {err}")