import mysql.connector

class ConnectionFactory():
    def getConexao(self):
        ##Estabelece e retorna uma conexão com o banco de dados MySQL.
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='AUMIGO',
            )
            return conexao
        except Exception as err:
            # Tratar o erro de conexão aqui, seja levantando uma exceção personalizada ou registrando o erro
            print(f"Erro ao conectar ao banco de dados: {err}")

    def fechar_conexao(self, conexao):
        ##Fecha a conexão com o banco de dados.
        if conexao.is_connected():
            conexao.close()