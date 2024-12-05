from PostDAO import PostDAO
from AnimalDAO import AnimalDAO
from UsuarioDAO import UsuarioDAO

postDAO = PostDAO()
animalDAO = AnimalDAO()
usuarioDAO = UsuarioDAO()

def apagarPost(post_id):
    postDAO.apagarPost(post_id)

def apagarAnimal(animal_id):
    animalDAO.apagarAnimal(animal_id)

usuario_id = None
usuarioDAO.apagarUsuario(usuario_id, apagarPost, apagarAnimal)
