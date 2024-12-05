from flask import Flask, render_template, request, redirect, flash , jsonify, make_response, url_for, Response
from Usuario import *
from UsuarioDAO import UsuarioDAO
from Animal import *
from AnimalDAO import *
from Post import *
from PostDAO import *
import secrets
import requests
import os
from requests.auth import HTTPDigestAuth
from datetime import timedelta
from flask import session
from gridfs import GridFS
from bson import ObjectId
from flask import send_file
from datetime import datetime
import locale
from apagar import apagarPost, apagarAnimal
locale.setlocale(locale.LC_TIME, 'portuguese')


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

collection = db["Animais"]
posts_collection = db['Posts'] 
usuario_collection = db['Usuarios']

fs = GridFS(db)

@app.route("/")
def index():
    animais = list(collection.find())
    postDAO=PostDAO()
    posts=postDAO.buscaPosts()
    for post in posts:
        post.dataCriacao = post.dataCriacao.strftime("%d/%m/%Y")
    return render_template("index.html" , animais=animais, posts=posts)

@app.route("/example")
def example():
    flash("Este é um exemplo de mensagem!", "successo")  
    flash("Outro aviso importante!", "erro")        
    return redirect(url_for("addAnimal")) 

@app.route("/inicio")
def inicio():
    collection = db["Animais"]
    animais = list(collection.find())
    postDAO=PostDAO()
    posts=postDAO.buscaPosts()
    for post in posts:
        post.dataCriacao = post.dataCriacao.strftime("%d/%m/%Y")
    return render_template("index.html" , animais=animais, posts=posts)

@app.route('/blog', defaults={"post_id": None})
@app.route('/blog/<string:post_id>')
def blog(post_id):
    postDAO = PostDAO()
    post=postDAO.buscaPostsPorIDs([post_id])
    print(post)
    if post_id is not None:
        print("foi aqui")
        print(post_id)

        return render_template('postTemplate.html', post=post, post_id=post_id, conteudo = post[0].get('conteudo'), data = post[0].get('dataCriacao').strftime("%d de %B de %Y, %H:%M"))

    else:
        posts = postDAO.buscaPosts()
        print("\033[31mPosts encontrados:\033[0;0m", posts)
        for post in posts:
            post.dataCriacao = post.dataCriacao.strftime("%d de %B de %Y, %H:%M")
            print(post.postID)
        return render_template('blog.html', posts=posts)


@app.route("/adotar/<animal_id>")
def adotar(animal_id):
    animal = collection.find_one({"_id": ObjectId(animal_id)})
    
    if animal:
        usuario = usuario_collection.find_one({"animais": ObjectId(animal_id)})
        
        if usuario:
           
            usuario_nome = usuario.get("nome")
            usuario_email = usuario.get("email")
        else:
            usuario_nome = "Usuário não encontrado"
            usuario_email = "teste@gmail.com"
        
        return render_template("adotar.html", animal=animal, usuario_nome=usuario_nome, usuario_email=usuario_email)
    else:
        return "Animal não encontrado", 404


@app.route("/animais", defaults={"tipo": None, "nome": None})
@app.route("/animais/<tipo>/", defaults={"nome": None})
@app.route("/animais/<tipo>/<nome>")
def animais(tipo, nome):
    if tipo is None and nome is None:
        animais = list(collection.find())
        return render_template("animais.html", animais=animais)
    
    if tipo is not None and nome is None:
        animais = list(collection.find({"tipo": tipo}))
        return render_template("animaisTemplate.html", tipo=tipo, animais=animais)
    
    else:
        animal_info = collection.find_one({"nome": nome})
        if animal_info:
            return render_template('animalTemplate.html', animal=animal_info)
        else:
            return "Animal não encontrado", 404

@app.route("/institucional")
def institucional():
    postDAO=PostDAO()
    posts=postDAO.buscaPosts()
    for post in posts:
        post.dataCriacao = post.dataCriacao.strftime("%d/%m/%Y")
    return render_template("institucional.html", posts=posts)   

@app.route("/favoritos")
def favoritos():
    return render_template("favoritos.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verificar")
def verificar():
    email = request.args.get("email-login").lower()
    print("Email akiiiii", email)
    password = str(request.args.get("password-login"))
    
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    if not email or not password:
        flash("Email ou Senha não fornecidos!", "erro")
        return render_template("login.html")  
    
    usuarioDAO = UsuarioDAO()
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
            
            resp = make_response(redirect(url_for('perfil')))
            resp.set_cookie('user', usuario.email, max_age=31536000) 
            return resp
        elif usuario.verificarUser == 'A':
            flash("Login como administrador!", "sucesso")
            usuarios = usuarioDAO.buscaUsuarios()
            for item in usuarios:
                print(item.nome)

            resp = make_response(redirect(url_for('perfil')))
            resp.set_cookie('admin', usuario.email, max_age=3600)  # Cookie válido por 1 hora
            return resp


@app.route("/cadastro")
def cadastro():
    email = request.args.get("email")
    password1 = request.args.get("password")
    password2 = request.args.get("confirm-password")
    if password1 != password2:
        flash("Senhas diferentes!", "erro")
        return render_template("login.html")
    password = password1

    usuarioDAO = UsuarioDAO()
    if usuarioDAO.buscaUsuarioPorEmail(email.upper()):
        flash("E-mail já cadastrado!", "erro")
        return render_template("login.html")

    usuario = Usuario(nome="Nome", email=email.upper(), senha=password, verificarUser="N", imgPerfil="static/images/person-1.png", desc="", animais=None, posts=None) #, imgPerfil="static/images/person-1.png", desc=""
    if usuarioDAO.insereUsuario(usuario):
        print(f"\033[32m\033[1mO Usuario {usuario.nome.upper()} foi adicionado com sucesso!\033[0;0m")
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/addAnimal", methods=["GET", "POST"])
def addAnimal():

    if request.method == "POST":
        nome = request.form.get("nome")
        #nome2 = request.form['nome']
        #print(request.form["nome"])
        tipo = request.form.get("tipo")
        raca = request.form.get("raca")
        genero = request.form.get("genero")
        nasc = request.form.get("nasc")
        desc = request.form.get("desc")
        status = request.form.get("status")
        foto = request.files.getlist("fotos")
        flash("Rota Acessada", "erro")

        if not nome or not tipo or not raca:
            flash("Por favor, preencha todos os campos obrigatórios.", "erro")
            return redirect(url_for("addAnimal"))
    
        animal = Animal(nome, tipo, raca, genero, nasc, desc, status, foto)
    
        userEmail = session.get('email')
        if not userEmail:
            flash("Erro: Usuário não autenticado.", "erro")
            return redirect(url_for("login"))
            
        animalDAO = AnimalDAO()
        if animalDAO.insereAnimal(animal, userEmail):
            flash("Animal Adicionado com Sucesso!", "sucesso")
            print("TO AKIIIIIIII!")
            #for v in request.form:
            #    print (f"{v},{request.form.get(v)}")
            return redirect(url_for("perfil"))
        else:
            print("Deu erro aki ein!")
            flash("Erro ao adicionar Animal", "erro")
            return redirect(url_for("addAnimal"))

    return render_template("addAnimal.html", today=datetime.today())

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
    usuario = usuarioDAO.buscaUsuarioPorEmail(userEmail)
    
    if not usuario:
        flash("Usuário não encontrado. Por favor, faça login novamente.", "erro")
        return redirect("/login")
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        desc = request.form.get("desc")
        imgPerfil = request.files.get("file")

        nome = nome.lower() if nome else usuario.nome.lower()
        email = email.upper() if email else usuario.email.upper()

        usuario.nome = nome
        usuario.email = email
        usuario.desc = desc
        
        # Se uma nova imagem de perfil foi carregada, a armazena
        if imgPerfil:
            # Converte a imagem em formato adequado e armazena no banco de dados
            image_id = fs.put(imgPerfil.read(), filename=imgPerfil.filename)
            usuario.imgPerfil = image_id  # Atualiza o ID da imagem no objeto do usuário
            print(f"\033[35m{str(usuario.imgPerfil)}\033[0;0m")

        if not usuarioDAO.alteraUsuario(usuario):
            flash("Erro ao atualizar o perfil.", "erro")
            return redirect(url_for('perfil'))
        
        flash("Perfil atualizado com sucesso!", "sucesso")

        # Atualiza o cookie se o email foi alterado
        resp = make_response(redirect(url_for('perfil')))
        if email != usuario.email:
            if request.cookies.get('user'):
                resp.set_cookie("user", usuario.email, max_age=60*60*24*365*10)  # Cookie vitalício (10 anos)
            elif request.cookies.get('admin'):
                resp.set_cookie("admin", usuario.email, max_age=60*60)  # Cookie de 1 hora
        
        return resp
    
    imgPerfil_url = url_for('image', image_id=usuario.imgPerfil)
    print(f"\033[32m{str(usuario.imgPerfil)}\033[0;0m")


    animais = animalDAO.buscaAnimaisPorUsuario(usuario.email)

    postDAO = PostDAO()
    posts = postDAO.buscaPostsPorUsuario(usuario.email)
    print(f"Posts associados ao usuário: {usuario.posts}")
    for post in posts:
        print(f"\033[33mPost: {post['_id']}\033[0m") 
    if usuario.verificarUser == "A":
        usuarios = usuarioDAO.buscaUsuarios()
        return render_template("perfil.html", usuario=usuario, animais=animais, imgPerfil_url=imgPerfil_url, posts=posts, administrador=usuario.verificarUser, usuarios=usuarios)
        
    if usuario.verificarUser == "N":
        return render_template("perfil.html", usuario=usuario, animais=animais, imgPerfil_url=imgPerfil_url, posts=posts)


@app.route('/apagar_usuario/<user_id>')
def apagar_usuario(user_id):
    usuarioDAO = UsuarioDAO()
    usuario_id = user_id
    if usuarioDAO.apagarUsuario(usuario_id, apagarPost, apagarAnimal):
        flash("Usuário apagado com sucesso!", "sucesso")
        return redirect(url_for("perfil"))
    else:
        flash("Erro ao apagar usuário.", "erro")
        return redirect(url_for("perfil"))


@app.route('/admin')
def admin():
    usuarioDAO = UsuarioDAO()
    userEmail = session.get('email')
    
    if not userEmail:
        return redirect(url_for('login'))
    
    usuario = usuarioDAO.buscaUsuarioPorEmail(userEmail)
    
    if not usuario:
        return redirect(url_for('login'))
    
    usuarios = usuarioDAO.buscaUsuarios()
    
    if hasattr(usuario, 'verificarUser'):
        return render_template('adm.html', administrador=usuario.verificarUser, usuarios=usuarios)
    else:
        return "Erro: A propriedade verificarUser não foi encontrada no usuário."


@app.route("/deletar_animal/<animal_id>", methods=["POST"])
def deletar_animal(animal_id):
    try:
        # Verifica se o animal_id é válido (não vazio)
        if not animal_id:
            flash("ID de animal inválido.", "erro")
            print(f"Erro ao receber animal_id: {animal_id}")
            return redirect("/perfil")


        animal = animalDAO.buscaAnimal(animal_id) 
        if not animal:
            flash("Animal não encontrado.", "erro")
            return redirect("/perfil")
        

        if animalDAO.apagarAnimal(animal_id):
            flash("Animal deletado com sucesso!", "sucesso")
        else:
            flash("Erro ao deletar animal.", "erro")
        
        return redirect("/perfil")

    except Exception as e:
        flash(f"Erro ao deletar animal: {str(e)}", "erro")
        print(f"Erro ao deletar animal: {str(e)}")
        return redirect("/perfil")


@app.route("/addPost", methods=["GET", "POST"])
def addPost():
    if request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"erro": "Nenhum dado JSON recebido"}), 400
            titulo = data.get('titulo')
            status = data.get('status')
            visibilidade = data.get('visibilidade')
            conteudo = data.get('conteudo')

            if not titulo or not status or not visibilidade or not conteudo:
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            usurioDAO = UsuarioDAO()
            userEmail = session.get('email')
            if not userEmail:
                return jsonify({"erro": "Usuário não autenticado"}), 401

            usuario = usurioDAO.buscaUsuarioPorEmail(userEmail)

            post = Post(titulo, status, visibilidade, conteudo, dataCriacao=datetime.now(), autor=usuario.nome)

            postDAO = PostDAO()
            if postDAO.adicionaPost(post, userEmail):
                return jsonify({"sucesso": "Post adicionado com sucesso!"}), 200
            else:
                return jsonify({"erro": "Erro ao adicionar o post"}), 500

        except Exception as e:
            print(f"Erro ao processar o post: {e}")
            return jsonify({"erro": "Erro interno no servidor"}), 500
    return render_template("addPost.html")


@app.route("/apagar_post/<post_id>", methods=["GET", "POST"])
def apagar_post(post_id):
    try:
        # Verifica se o post_id é válido (não vazio)
        if not post_id:
            flash("ID de post inválido.", "erro")
            print(f"Erro ao receber post_id: {post_id}")
            return redirect("/perfil")


        postDAO = PostDAO()
        post = postDAO.buscaPost(post_id) 
        if not post:
            flash("Post não encontrado.", "erro")
            return redirect("/perfil")
        

        if postDAO.apagarPost(post_id):
            flash("Post deletado com sucesso!", "sucesso")
        else:
            flash("Erro ao deletar post.", "erro")
        
        return redirect("/perfil")

    except Exception as e:
        flash(f"Erro ao deletar post: {str(e)}", "erro")
        print(f"Erro ao deletar post: {str(e)}")
        return redirect("/perfil")


@app.route('/getPost/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db.posts_collection.find_one({"_id": ObjectId(post_id)})
    
    if post:
        return jsonify({
            '_id': str(post['_id']),
            'titulo': post['titulo'],
            'conteudo': post['conteudo'],  # Aqui retorna o conteúdo com as tags HTML intactas
            'status': post['status'],
            'visibilidade': post['visibilidade'],
            'autor': post['autor']
        })
    else:
        return jsonify({'erro': 'Post não encontrado'}), 404


'''
@app.route("/post/<action>", methods=["GET", "POST"])
def post(action):
    if request.method == "POST":
        try:
            # Validar ação (adicionar ou editar)
            if action not in ["adicionar", "editar"]:
                return jsonify({"erro": "Ação inválida"}), 400

            data = request.get_json()
            if not data:
                return jsonify({"erro": "Nenhum dado JSON recebido"}), 400

            # Extrair campos do JSON
            titulo = data.get('titulo')
            status = data.get('status')
            visibilidade = data.get('visibilidade')
            conteudo = data.get('conteudo')

            if not titulo or not status or not visibilidade or not conteudo:
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            # Verificar usuário autenticado
            usuarioDAO = UsuarioDAO()
            userEmail = session.get('email')
            if not userEmail:
                return jsonify({"erro": "Usuário não autenticado"}), 401

            usuario = usuarioDAO.buscaUsuarioPorEmail(userEmail)
            postDAO = PostDAO()

            if action == "adicionar":
                # Criar novo post
                post = Post(
                    titulo=titulo,
                    status=status,
                    visibilidade=visibilidade,
                    conteudo=conteudo,
                    dataCriacao=datetime.now(),
                    autor=usuario.nome
                )

                if postDAO.adicionaPost(post, userEmail):
                    return jsonify({"sucesso": "Post adicionado com sucesso!"}), 200
                else:
                    return jsonify({"erro": "Erro ao adicionar o post"}), 500

            elif action == "editar":
                # Buscar post_id do JSON
                post_id = data.get('post_id')
                if not post_id:
                    return jsonify({"erro": "ID do post ausente"}), 400

                # Buscar o post original
                post = postDAO.buscaPostPorId(post_id, userEmail)
                if not post:
                    return jsonify({"erro": "Post não encontrado"}), 404

                # Atualizar campos permitidos
                post.titulo = titulo
                post.status = status
                post.visibilidade = visibilidade
                post.conteudo = conteudo
                print(post)

                if postDAO.editarPost(post, userEmail):
                    return jsonify({"sucesso": "Post editado com sucesso!"}), 200
                else:
                    return jsonify({"erro": "Erro ao editar o post"}), 500

        except Exception as e:
            print(f"Erro ao processar a ação '{action}' do post: {e}")
            return jsonify({"erro": "Erro interno no servidor"}), 500

    # Renderizar a página HTML para adicionar/editar posts
    if action == "adicionar":
        return render_template("addPost.html")
    elif action == "editar":
        post_id = request.args.get('post_id')  # Capturar o post_id via query string
        return render_template("addPost.html", post_id=post_id)'''


@app.route('/image/<image_id>')
def image(image_id):
    try:
        image_file = fs.get(ObjectId(image_id))
        return image_file.read(), 200, {'Content-Type': 'image/jpeg'}
    except:
        return "\033[31mImage not found\033[0;0m", 404

if __name__ == '__main__':
    app.run(debug=True)


