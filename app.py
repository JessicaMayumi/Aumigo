from flask import Flask, render_template, request, redirect, flash , jsonify, make_response 
from Usuario import *
from UsuarioDAO import *
import secrets
import requests
import os
from requests.auth import HTTPDigestAuth
from datetime import timedelta

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/institucional")
def institucional():
    return render_template("institucional.html")

@app.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verificar")
def verificar():
    email = request.args.get("email-login").upper()
    password = str(request.args.get("password-login")).upper()
    
    #Mensagens de depuração
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    if not email or not password:
        flash("Email ou Senha não fornecidos!", "erro")
        return render_template("login.html")  
    
    usuario = usuarioDAO.buscaUsuario(email, password)
    
    if usuario is None:
        flash("Email ou Senha inválido!", "erro")
        return render_template("login.html")  
    else:
        if usuario.verificarUser == 'N':
            flash("Login realizado com sucesso!", "sucesso")
            #https://www.hashtagtreinamentos.com/usar-cookies-com-python
            flash("Login realizado com sucesso!", "sucesso")
            resp = make_response(render_template("perfil.html", usuario=usuario))
            resp.set_cookie('user', usuario.email, max_age=31536000)  # Cookie válido por 1 ano
            return resp
        elif usuario.verificarUser == 'A':
            flash("Login como administrador!", "sucesso")
            usuarios = usuarioDAO.buscaUsuarios()
            for item in usuarios:
                print(item.nome)  # Exibe o nome dos usuários no terminal
            resp = make_response(render_template("adm.html", administrador=usuario.verificarUser, usuarios=usuarios))
            resp.set_cookie('admin', usuario.email, max_age=3600)  # Cookie válido por 1 hora
            return resp

@app.route("/cadastro")
def cadastro():
    email = request.args.get("email")
    password = request.args.get("password")
    usuario = Usuario(nome="May", email=email.upper(), senha=password, verificarUser="N")
    if usuarioDAO.insereUsuario(usuario):
        print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/animais")
def animais():
    return render_template("animais.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/addAnimal")
def addAnimal():
    return render_template("addAnimal.html")

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    # Obtém o cookie do usuário
    user_cookie = request.cookies.get('user') or request.cookies.get('admin')
    
    if not user_cookie:
        flash("Nenhum cookie ativo encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    usuario = usuarioDAO.buscaUsuarioPorEmail(user_cookie)
    
    if not usuario:
        flash("Usuário não encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email").upper()
        descricao = request.form.get("descricao")
        foto = request.files.get("foto")

        if foto:
            foto_path = os.path.join('static/uploads/', foto.filename)
            foto.save(foto_path)
            usuario.foto = foto_path


        usuario.nome = nome
        usuario.descricao = descricao
        
        # Verifica se o email foi alterado
        email_alterado = usuario.email != email
        usuario.email = email

        usuarioDAO.alteraUsuario(usuario)
        flash("Perfil atualizado com sucesso!", "sucesso")

        resp = make_response(redirect("/perfil"))
        
        # Atualiza o cookie se o email foi alterado
        if email_alterado:
            if request.cookies.get('user'):
                resp.set_cookie("user", usuario.email, max_age=60*60*24*365*10)  # Cookie vitalício (10 anos)
            elif request.cookies.get('admin'):
                resp.set_cookie("admin", usuario.email, max_age=60*60)  # Cookie de 1 hora
        
        return resp

    # Obtém a lista de animais do usuário
    #animais = usuarioDAO.buscaAnimaisPorUsuario(usuario.email)

    return render_template("perfil.html", usuario=usuario) #, animais=animais


@app.route("/deletar_animal/<animal_id>", methods=["POST"])
def deletar_animal(animal_id):
    if usuarioDAO.deletaAnimal(animal_id):
        flash("Animal deletado com sucesso!", "sucesso")
    else:
        flash("Erro ao deletar animal.", "erro")
    return redirect("/perfil")


"""
@app.route('/users', methods=['GET'])
def users():
    api_key = 'vWz2GhWRTlcMS3yRF5zuWkqbKokTF6TgiLWxLHgh2ybbZXmKAQSCJZNVY6D7i4Ut'
    url = 'https://sa-east-1.aws.data.mongodb-api.com/app/data-appojul/endpoint/data/v1/action/findOne'
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }
    data = {
        "collection": "Usuarios",
        "database": "AUMIGO",
        "dataSource": "AUMIGO",
        "projection": {"_id": 1, "nome": 1, "email": 1}
    }

    #proxies = {
    #'http': os.getenv('HTTP_PROXY'),
    #'https': os.getenv('HTTPS_PROXY'),
    #}
    response = requests.post(url, headers=headers, json=data) #, proxies=proxies
    if response.status_code == 200:
        response_data = response.json()
        print("Dados do Objeto Retornado:")
        print(response_data)
        return jsonify(response_data)
    else:
        #return jsonify({"error": response.status_code, "message": response.text}), response.status_code
        print("Erro:", response.status_code, response.json())


# https://www.youtube.com/watch?v=FBLAV1SbJFk

"""