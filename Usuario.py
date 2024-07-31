class Usuario():
    def __init__(self, nome, email, senha, verificarUser, usuarioID = None):
        self.__email = email
        self.__nome = nome
        self.__senha = senha
        self.__verificarUser = verificarUser
        self.__usuarioID = usuarioID
  
    @property
    def email(self):
        return self.__email
 
    @email.setter
    def email(self, email):
        self.__email = email
 
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome 

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.__senha = senha 

    @property
    def verificarUser(self):
        return self.__verificarUser
    
    @verificarUser.setter
    def verificarUser(self, verificarUser):
        self.__verificarUser = verificarUser 

    @property
    def usuarioID(self):
        return self.__usuarioID
    
    @usuarioID.setter
    def usuarioID(self,usuarioID):
        self.usuarioID = usuarioID

    def __str__(self): 
        return f"Nome: {self.__nome}\nEmail: {self.__email}\nID: {self.__usuarioID}"
    
    '''   def imprimirLado(self):
        restaurante = RestauranteDAO().buscaRestaurante(self.__restauranteID)
        # print(f"{dado[0]:<30}{dado[1]:>3} anos")
        return f"\033[1m\033[36m| {self.__nome:<32}| {self.__cargo:<16}| {str(self.__salario):<11}| \033[33m\033[1m{str(self.__cpf):<16}\033[1m\033[36m| {dataFormatada(self.__dataContratacao):<14}| \033[36m{restaurante.nome:<36} |\033[0;0m"
'''
# converter data pt-BR para SQL
# data = datetime.strptime('26/08/2018', '%d/%m/%Y').date()
# print(data)
# usuario = Usuario("a", "b", 12.23, 123, "2006-06-06", 1)
# usuario = Usuario("a", "b", 12.23, 123, "10/10/1991", 1)
# print(usuario)


