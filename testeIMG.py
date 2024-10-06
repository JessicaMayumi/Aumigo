from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from UsuarioDAO import UsuarioDAO
import os

app = Flask(__name__)

# Pasta onde as imagens serão temporariamente armazenadas
import gridfs

# Salvando a imagem no GridFS em vez de localmente
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'imgPerfil' not in request.files:
        flash('Nenhum arquivo foi selecionado')
        return redirect(request.url)
    
    file = request.files['imgPerfil']
    
    if file.filename == '':
        flash('Nenhum arquivo foi selecionado')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Armazenar a imagem no GridFS
        usuarioDAO = UsuarioDAO()
        img_data = file.read()  # Lê o arquivo
        img_id = usuarioDAO.fs.put(img_data, filename=file.filename)  # Salva no GridFS
        
        # Atualiza o banco de dados com o ID da nova imagem
        usuario = usuarioDAO.buscaUsuarioPorEmail(request.form['email'])
        
        if usuario:
            usuario.imgPerfil = str(img_id)  # Armazena o ID da imagem no GridFS
            usuarioDAO.alteraUsuario(usuario)  # Atualiza no banco de dados
            flash('Perfil atualizado com sucesso!')
        else:
            flash('Erro ao atualizar perfil.')
        
        return redirect(url_for('perfil'))  # Redireciona para a página de perfil

    flash('Arquivo não permitido. Por favor, envie uma imagem válida.')
    return redirect(request.url)
