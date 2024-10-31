class Animal():
    def __init__(self, nome, tipo, raca, genero, nasc, desc, status, foto, animalID = None):
        self.__nome = nome
        self.__tipo = tipo
        self.__raca = raca
        self.__genero = genero
        self.__nasc = nasc
        self.__desc = desc
        self.__status = status
        self.__foto = foto
        self.__animalID = animalID
  
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.nome = nome

    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo

    @property
    def raca(self):
        return self.__raca
    
    @raca.setter
    def raca(self, raca):
        self.__raca = raca

    @property
    def genero(self):
        return self.__genero
    
    @genero.setter
    def genero(self, genero):
        self.__genero = genero

    @property
    def nasc(self):
        return self.__nasc
    
    @nasc.setter
    def nasc(self, nasc):
        self.__nasc = nasc

    @property
    def desc(self):
        return self.__desc
    
    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def foto(self):
        return self.__foto
    
    @foto.setter
    def foto(self, foto):
        self.__foto = foto

    @property
    def animalID(self):
        return self.__animalID
    
    @animalID.setter
    def usuarioID(self,animalID):
        self.animalID = animalID

    def __str__(self): 
        return f"Nome: {self.__nome}\nTipo de Animal: {self.__tipo}\nRaça: {self.__raca}\nGênero: {self.__genero}\nnasc: {self.__nasc}\nDescrição: {self.__desc}\nStatus: {self.__status}\nID: {self.__animalID}"