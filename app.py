from flask import Flask, render_template, request, redirect, flash , jsonify, make_response, url_for
from Usuario import *
from UsuarioDAO import *
from Animal import *
from AnimalDAO import *
import secrets
import requests
import os
from requests.auth import HTTPDigestAuth
from datetime import timedelta
from flask import session

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    return render_template("index.html")

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
    email = request.args.get("email-login").lower()
    password = str(request.args.get("password-login"))
    
    #Mensagens de depuração
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    if not email or not password:
        flash("Email ou Senha não fornecidos!", "erro")
        return render_template("login.html")  
    
    usuario = usuarioDAO.buscaUsuario(email, password)
    
    if usuario == None:
        flash("Email ou Senha inválido!", "erro")
        return render_template("login.html")  
    else:
        session['email'] = usuario.email
        print(f"Usuário encontrado: {usuario.nome}, Tipo: {usuario.verificarUser}, Img: {usuario.imgPerfil}")
        if usuario.verificarUser == 'N':
            flash("Login realizado com sucesso!", "sucesso")
            #https://www.hashtagtreinamentos.com/usar-cookies-com-python
            flash("Login realizado com sucesso!", "sucesso")
            animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)
            print(f"\033[0;32mAnimais encontrados: {animais}\033[0;0m")
            if not animais:
                print("Nenhum animal encontrado para este usuário.")
            resp = make_response(render_template("perfil.html", usuario=usuario, animais=animais))
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
    usuario = Usuario(nome="May", email=email.upper(), senha=password, verificarUser="N") #, imgPerfil="static/images/person-1.png", desc=""
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

@app.route("/addAnimal", methods=["GET", "POST"])
def addAnimal():

    if request.method == "POST":
        nome = request.form.get("nome")
        tipo = request.form.get("tipo")
        raca = request.form.get("raca")
        genero = request.form.get("genero")
        nasc = request.form.get("nasc")
        desc = request.form.get("desc")
        status = request.form.get("status")
        foto = request.form.get("foto")

        if not nome or not tipo or not raca:
            flash("Por favor, preencha todos os campos obrigatórios.", "erro")
            return redirect(url_for("/addAnimal"))
        
        animalDAO = AnimalDAO()
        animal = Animal(nome, tipo, raca, genero, nasc, desc, status, foto=None)
        
        userEmail = session.get('email')
        if not userEmail:
            flash("Erro: Usuário não autenticado.", "erro")
            return redirect(url_for("/login"))
        
        if animalDAO.insereAnimal(animal, userEmail):
            flash("Animal Adicionado com Sucesso!", "sucesso")
            return redirect(url_for("/perfil"))
        else:
            flash("Erro ao adicionar Animal", "erro")
            return redirect("/addAnimal")
    
    return render_template("addAnimal.html")


@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    userEmail = session.get('email')  # Recupera o email da sessão
    if not userEmail:
        flash("Erro: Usuário não autenticado.", "erro")
        return redirect("/login")

    # Obtém o cookie do usuário
    user_cookie = request.cookies.get('user') or request.cookies.get('admin')
    print("62622612561612111.")
    if not user_cookie:
        flash("Nenhum cookie ativo encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    usuarioDAO = UsuarioDAO()
    animalDAO = AnimalDAO()
    usuario = usuarioDAO.buscaUsuarioPorEmail(user_cookie)
    print(f"Usuário encontrado: {usuario}")
    
    if not usuario:
        flash("Usuário não encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        desc = request.form.get("desc")
        imgPerfil = request.files.get("imgPerfil")

        # Verifica se o nome não é None antes de usar .lower()
        nome = nome.lower() if nome else usuario.nome.lower()
        # Verifica se o email não é None antes de usar .upper()
        email = email.upper() if email else usuario.email.upper()

#        if imgPerfil:
#            # Armazena a foto no GridFS
#            img_id = usuario.salvaImagem(imgPerfil)  #-----------------------------
#            usuario.imgPerfil = img_id  # Armazena o ID do GridFS no usuário

        usuario.nome = nome
        usuario.desc = desc
        
        # Verifica se o email foi alterado
        email_alterado = usuario.email != email
        usuario.email = email

        if not usuarioDAO.alteraUsuario(usuario):
            flash("Erro ao atualizar o perfil.", "erro")
            return redirect(url_for("/perfil"))
        
        flash("Perfil atualizado com sucesso!", "sucesso")

        resp = make_response(redirect("/perfil"))
        
        # Atualiza o cookie se o email foi alterado
        if email_alterado:
            if request.cookies.get('user'):
                resp.set_cookie("user", usuario.email, max_age=60*60*24*365*10)  # Cookie vitalício (10 anos)
            elif request.cookies.get('admin'):
                resp.set_cookie("admin", usuario.email, max_age=60*60)  # Cookie de 1 hora
        
        return resp
    
    animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)
    print(f"\033[0;32mAnimais encontrados: {animais}\033[0;0m")
    if not animais:
        print("Nenhum animal encontrado para este usuário.")

    return render_template("perfil.html", usuario=usuario, animais=animais)

    
@app.route('/imagem/<img_id>')
def serve_imagem(img_id):
    try:
        grid_out = usuarioDAO.fs.get(ObjectId(img_id))
        response = make_response(grid_out.read())
        response.headers['Content-Type'] = grid_out.content_type
        print(f"Imagem servida com ID: {img_id}")
        return response
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return 'Erro ao carregar a imagem', 500

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