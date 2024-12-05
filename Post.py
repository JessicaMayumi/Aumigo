class Post:
    def __init__(self, titulo, status, visibilidade, conteudo, dataCriacao, autor, postID = None):
        self.__titulo = titulo
        self.__status = status
        self.__visibilidade = visibilidade
        self.__conteudo = conteudo
        self.__dataCriacao = dataCriacao
        self.__autor = autor 
        self.__postID = postID

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def visibilidade(self):
        return self.__visibilidade

    @visibilidade.setter
    def visibilidade(self, visibilidade):
        self.__visibilidade = visibilidade

    @property
    def conteudo(self):
        return self.__conteudo

    @conteudo.setter
    def conteudo(self, conteudo):
        self.__conteudo = conteudo

    @property
    def dataCriacao(self):
        return self.__dataCriacao
    
    @dataCriacao.setter
    def dataCriacao(self, dataCriacao):
        self.__dataCriacao = dataCriacao  

    @property
    def autor(self):
        return self.__autor
    
    @autor.setter
    def autor(self, autor):
        self.__autor = autor  

    @property
    def postID(self):
        return self.__postID

    def __str__(self):
        return f"Titulo: {self.__titulo}\nStatus: {self.__status}\nID: {self.__postID}"