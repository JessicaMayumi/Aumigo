from bson.binary import Binary
from pymongo import MongoClient


class ImagemManager:
    def __init__(self, db_name='AUMIGO', mongo_uri='mongodb+srv://AUMIGO:MAY@aumigo.ziyhr.mongodb.net/?authMechanism=SCRAM-SHA-1&ssl=true'):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def salvaImagem(self, foto, user_id):
        try:
            img_data = foto.read()  # Lê os dados da imagem
            self.db.imagens.insert_one({
                'user_id': user_id,
                'filename': foto.filename,
                'image': Binary(img_data)
            })  # Salva a imagem na coleção
            print(f"Imagem salva com o nome: {foto.filename} para o usuário: {user_id}")
            return foto.filename  # Retorna o nome do arquivo salvo
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")
            return None

# Exemplo de uso:
# manager = ImagemManager()
# with open('/path/to/your/image.jpg', 'rb') as foto:
#     manager.salvaImagem(foto, 'user123')