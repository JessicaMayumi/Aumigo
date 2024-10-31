from flask import Flask, request, render_template
import bson
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection  
from pymongo.database import Database

load_dotenv()
connection_string: str = os.environ.get("CONNECTION_STRING")
mongo_client: MongoClient = MongoClient(connection_string)

database: Database = mongo_client.get_database("AUMIGO")
collection: Collection = database.get_collection("Users")

'''user = { 
    "nome" : "May",
    "password" : "123",
    "email" : "may@gmail.com"
}

collection.insert_one(user)
'''
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#Criar e Ler

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        #Criar
        nome : str = request.json["nome"]
        password : str = request.json["password"]
        email: str = request.json["email"]

        #inserir
        collection.insert_one({"nome" : nome,
                               "password" : password,
                               "email" : email})

        return f"O user {nome} foi criado! Senha: {password} e Email: {email}"    

    elif request.method == "GET":
        #LER
        aumigo = list(collection.find())
        usuarios = []

        for nomes in aumigo:
            nome = nomes["nome"]
            password = nomes["password"]
            email = nomes ["email"]
            usuario = {
                "nome" : nome,
                "password" : password,
                "email" : email
            }

            usuarios.insert(0, usuario)

        return usuarios

#UPDATE
@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id: str):
    novoNome: str = request.json["nome"]
    novaSenha: str = request.json["password"]    
    novoEmail: str = request.json["email"]
    collection.update_one({"_id" : bson.ObjectId(user_id)}, {"$set" : {"nome" : novoNome, "password" : novaSenha, "email" : novoEmail} })

    return f"UPDATE: o nome do usuario foi atualizado para {novoNome}, senha: {novaSenha}, email: {novoEmail}"



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
        imgPerfil = request.files.get("imgPerfil")

        # Verifica se o nome não é None antes de usar .lower()
        nome = nome.lower() if nome else usuario.nome.lower()
        # Verifica se o email não é None antes de usar .upper()
        email = email.upper() if email else usuario.email.upper()

        # Salvar a imagem de perfil se fornecida
        if imgPerfil:
            img_id = usuario.salvaImagem(imgPerfil)  # Armazena a foto no GridFS
            usuario.imgPerfil = img_id  # Armazena o ID do GridFS no usuário

        usuario.nome = nome
        usuario.desc = desc
        
        # Verifica se o email foi alterado
        email_alterado = usuario.email != email
        usuario.email = email

        if not usuarioDAO.alteraUsuario(usuario):
            flash("Erro ao atualizar o perfil.", "erro")
            return redirect(url_for('perfil', usuario_id=usuario_id))
        
        flash("Perfil atualizado com sucesso!", "sucesso")

        resp = make_response(redirect("perfil", usuario_id=usuario_id))
        
        # Atualiza o cookie se o email foi alterado
        if email_alterado:
            if request.cookies.get('user'):
                resp.set_cookie("user", usuario.email, max_age=60*60*24*365*10)  # Cookie vitalício (10 anos)
            elif request.cookies.get('admin'):
                resp.set_cookie("admin", usuario.email, max_age=60*60)  # Cookie de 1 hora
        
        return resp
    
    # Obtém os animais do usuário
    animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)
    if not animais:
        print("Nenhum animal encontrado para este usuário.")

    # Obtenha a imagem de perfil se houver
    img_perfil = None
    if usuario.imgPerfil:
        img_query = {"_id": ObjectId(usuario.imgPerfil)}
        imagem = collection.find_one(img_query)
        if imagem:
            img_perfil = BytesIO(imagem['data'])  # Supondo que a imagem esteja armazenada como binário na chave 'data'

    # Renderiza o template do perfil com os dados do usuário e animais
    return render_template("perfil.html", usuario=usuario, animais=animais, img_perfil=img_perfil)


#DELETAR

@app.route("/users/<string:user_id>", methods=["DELETE"])
def revomer_user(user_id: str):
    collection.delete_one({"_id" : bson.ObjectId(user_id)})

    return f"DELETADO: O usuario (id = {user_id}) foi removido"

""""animal = [
    {
        "id" : 1,
        "nome" : "pompom",
        "tipo": "gato"
    }, 
    {
        "id" : 2,
        "nome" : "rabito",
        "tipo": "coelho"
    }, 
    {
        "id" : 3,
        "nome" : "lua",
        "tipo": "cachorro"
    }, 
]

@app.route("/animal")
def obter_animais():
    return jsonify(animal)"""