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
from gridfs import GridFS
from bson import ObjectId
from flask import send_file


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

collection = db["Animais"]

fs = GridFS(db)

@app.route("/")
def index():
    animais = list(collection.find())
    return render_template("index.html" , animais=animais)

@app.route("/inicio")
def inicio():
    collection = db["Animais"]
    animais = list(collection.find())
    return render_template("index.html" , animais=animais)

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/animais", defaults={"tipo": None, "nome": None})
@app.route("/animais/<tipo>/", defaults={"nome": None})
@app.route("/animais/<tipo>/<nome>")
def animais(tipo, nome):
    if tipo is None and nome is None:
        animais = list(collection.find())
        return render_template("animais.html" , animais=animais)
    if tipo is not None and nome is None:
        animais = list(collection.find({"tipo": tipo}))
        return render_template("animaisTemplate.html", tipo=tipo, animais=animais)
    else:
        animal_info = collection.find_one({"nome": nome})  # Busca animal específico pelo nome
        if animal_info:
            return render_template('animalTemplate.html', animal=animal_info)
        else:
            return "Animal não encontrado", 404

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
            animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)
            print(f"\033[0;32mAnimais encontrados: {animais}\033[0;0m")
            if not animais:
                print("Nenhum animal encontrado para este usuário.")
            
            # Redireciona para a rota de perfil em vez de renderizar o template diretamente
            resp = make_response(redirect(url_for('perfil')))
            resp.set_cookie('user', usuario.email, max_age=31536000)  # Cookie válido por 1 ano
            return resp
        elif usuario.verificarUser == 'A':
            flash("Login como administrador!", "sucesso")
            usuarios = usuarioDAO.buscaUsuarios()
            for item in usuarios:
                print(item.nome)  # Exibe o nome dos usuários no terminal
            # Redireciona para a rota de administração em vez de renderizar o template diretamente
            resp = make_response(redirect(url_for('adm')))  # Supondo que você tenha uma rota chamada 'adm'
            resp.set_cookie('admin', usuario.email, max_age=3600)  # Cookie válido por 1 hora
            return resp


@app.route("/cadastro")
def cadastro():
    email = request.args.get("email")
    password = request.args.get("password")
    usuario = Usuario(nome="May", email=email.upper(), senha=password, verificarUser="N", imgPerfil="static/images/person-1.png", desc="", animais=None) #, imgPerfil="static/images/person-1.png", desc=""
    if usuarioDAO.insereUsuario(usuario):
        print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")
        return render_template("index.html")
    else:
        return render_template("login.html")

'''@app.route('/animal')
def animal():
    return render_template('teste.html')'''

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
        
        animal = Animal(nome, tipo, raca, genero, nasc, desc, status, foto)
        
        userEmail = session.get('email')
        if not userEmail:
            flash("Erro: Usuário não autenticado.", "erro")
            return redirect(url_for("login"))
            
        animalDAO = AnimalDAO()
        if animalDAO.insereAnimal(animal, userEmail):
            flash("Animal Adicionado com Sucesso!", "sucesso")
            return redirect(url_for("perfil"))
        else:
            flash("Erro ao adicionar Animal", "erro")
            return redirect(url_for("addAnimal"))
    
    return render_template("addAnimal.html")

@app.route("/perfil", defaults={"usuario_id": None})
@app.route("/perfil/<usuario_id>", methods=["GET", "POST"])
def perfil(usuario_id):
    userEmail = session.get('email')  # Recupera o email da sessão
    if not userEmail:
        flash("Erro: Usuário não autenticado.", "erro")
        return redirect("/login")

    # Obtém o cookie do usuário
    user_cookie = request.cookies.get('user') or request.cookies.get('admin')
    if not user_cookie:
        flash("Nenhum cookie ativo encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    usuarioDAO = UsuarioDAO()
    animalDAO = AnimalDAO()
    usuario = usuarioDAO.buscaUsuarioPorEmail(user_cookie)
    
    if not usuario:
        flash("Usuário não encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        desc = request.form.get("desc")
        imgPerfil = request.files.get("file")  # A imagem agora vem do campo 'file'

        # Verifica se o nome não é None antes de usar .lower()
        nome = nome.lower() if nome else usuario.nome.lower()
        # Verifica se o email não é None antes de usar .upper()
        email = email.upper() if email else usuario.email.upper()

        # Atualiza as informações do usuário
        usuario.nome = nome
        usuario.email = email
        usuario.desc = desc
        
        # Se uma nova imagem de perfil foi carregada, a armazena
        if imgPerfil:
            # Converte a imagem em formato adequado e armazena no banco de dados
            image_id = fs.put(imgPerfil.read(), filename=imgPerfil.filename)
            usuario.imgPerfil = image_id  # Atualiza o ID da imagem no objeto do usuário
            print(f"\033[35m{str(usuario.imgPerfil)}\033[0;0m")

        # Atualiza o usuário no banco de dados
        if not usuarioDAO.alteraUsuario(usuario):
            flash("Erro ao atualizar o perfil.", "erro")
            return redirect(url_for('perfil'))
        
        flash("Perfil atualizado com sucesso!", "sucesso")

        # Atualiza o cookie se o email foi alterado
        resp = make_response(redirect(url_for('perfil')))
        if email != usuario.email:  # Verifica se o email foi alterado
            if request.cookies.get('user'):
                resp.set_cookie("user", usuario.email, max_age=60*60*24*365*10)  # Cookie vitalício (10 anos)
            elif request.cookies.get('admin'):
                resp.set_cookie("admin", usuario.email, max_age=60*60)  # Cookie de 1 hora
        
        return resp
    
    imgPerfil_url = url_for('image', image_id=usuario.imgPerfil)
    print(f"\033[32m{str(usuario.imgPerfil)}\033[0;0m")

    # Busca os animais do usuário
    animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)
    return render_template("perfil.html", usuario=usuario, animais=animais, imgPerfil_url=imgPerfil_url)





@app.route("/deletar_animal/<animal_id>", methods=["POST"])
def deletar_animal(animal_id):
    if usuarioDAO.deletaAnimal(animal_id):
        flash("Animal deletado com sucesso!", "sucesso")
    else:
        flash("Erro ao deletar animal.", "erro")
    return redirect("/perfil")

@app.route('/image/<image_id>')
def image(image_id):
    try:
        image_file = fs.get(ObjectId(image_id))
        return image_file.read(), 200, {'Content-Type': 'image/jpeg'}
    except:
        return "\033[31mImage not found\033[0;0m", 404

if __name__ == '__main__':
    app.run(debug=True)



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