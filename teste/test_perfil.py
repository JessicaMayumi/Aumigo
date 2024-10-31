import sys
import os
import unittest
from flask import Flask
from io import BytesIO
from werkzeug.datastructures import MultiDict

# Adicionar o diretório do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, usuarioDAO
from Usuario import Usuario

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'  # Você pode usar 'filesystem' ou 'memcached'
app.config['SECRET_KEY'] = 'secret_key'  # Defina uma chave secreta para a sessão

class TestPerfil(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Crie um usuário de teste se não existir
        self.usuario_email = "test@example.com"
        self.usuario_senha = "password"
        
        # Verifica se o usuário já existe
        self.usuario = usuarioDAO.buscaUsuario(self.usuario_email, self.usuario_senha)
        if not self.usuario:
            # Insere o usuário de teste
            novo_usuario = Usuario(
                nome="Test User",
                email=self.usuario_email,
                senha=self.usuario_senha,
                verificarUser="N",
                imgPerfil="static/images/person-1.png",
                desc="Test description"
            )
            usuarioDAO.insereUsuario(novo_usuario)
            self.usuario = usuarioDAO.buscaUsuario(self.usuario_email, self.usuario_senha)

        # Configura o cookie do usuário diretamente na instância do cliente de teste
        self.app.set_cookie('localhost', 'user', self.usuario.email)

    def login_user(self, email):
        with self.app.session_transaction() as sess:
            sess['user'] = email

    def test_alterar_imagem_perfil(self):
        # Prepare o arquivo de imagem
        img_data = BytesIO(b"test image data")
        
        # Crie o formulário de dados
        form_data = MultiDict({
            "nome": "Updated User",
            "email": "updated@example.com",
            "descricao": "Updated description"
        })
        
        # Adicione a foto ao formulário
        files = {
            "foto": (img_data, "test_image.jpg")
        }
        
        # Faça a requisição POST para alterar o perfil
        response = self.app.post("/perfil", data={**form_data, **files}, content_type="multipart/form-data", follow_redirects=True)
        
        # Adicione mensagens de depuração
        print("Status Code:", response.status_code)
        print("Response Data:", response.data.decode('utf-8'))

        # Verifique se o status é 302 (redirecionamento)
        self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()