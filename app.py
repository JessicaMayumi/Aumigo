from flask import Flask, render_template, request, redirect
from Usuario import *
from UsuarioDAO import *

app = Flask(__name__)

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

@app.route("/cadastro")
def cadastro():
    email = request.args.get("email")
    password = request.args.get("password")
    usuario = Usuario("May", email.upper(), password, "N")
    if usuarioDAO.insereUsuario(usuario): #Inserir Funcionando
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