from django.shortcuts import render, redirect
from core.models import PostModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages

def home( request ):
    posts = PostModel.objects.all()
    
    return render(request, "index.html", {"posts": posts})

def post(request, id):
    post = PostModel.objects.filter(id=id).first()
    
    return render(request, "post.html", {"post": post})

def criar_post(request):
    if not request.user.is_authenticated:
        return redirect("login")
        
    if request.method == "POST":
        titulo = request.POST["titulo"]
        conteudo = request.POST["conteudo"]
        
        post = PostModel.objects.create(titulo=titulo, conteudo=conteudo, user=request.user)
        post.save()
             
    return render(request, "criarpost.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        usuario = request.POST["usuario"]
        password = request.POST["senha"]
        
        if usuario == "" or password == "":
            messages.error(request, "Os campos usuario e senha não podem ser vazios")
            return redirect("login")
        
        if User.objects.filter(username=usuario).exists():
            user = authenticate(request, username=usuario, password=password)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login feito com sucesso")
                return redirect("home")
                
            else:
                messages.error(request, "Usuario ou senha invalidos")
                return redirect("login")
                
        else:
            messages.error(request, "Usuario inexistente")
            return redirect("login")
    
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("home")

def cadastro(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        usuario = request.POST["usuario"]
        email = request.POST["email"]
        primeiro_nome = request.POST["primeiro_nome"]
        segundo_nome = request.POST["segundo_nome"]
        senha = request.POST["senha"]
        confirmar_senha = request.POST["confirmar_senha"]
        
        if usuario == "" or email == "" or primeiro_nome == "" or segundo_nome == "" or senha == "":
            messages.error(request, "Todos os campos são obrigatorios")
            return redirect("cadastro")
        
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem")
            return redirect("cadastro")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Usuario com esse email ja existe")
            return redirect("cadastro")
        
        if User.objects.filter(username=usuario).exists():
            messages.error(request, "Usuario com esse username ja existe")
            return redirect("cadastro")
        
        user = User.objects.create_user(
            username=usuario,
            email=email,
            first_name=primeiro_nome,
            last_name=segundo_nome,
            password=senha
        )
        
        user.save()
        
        messages.success(request, "Usuario cadastrado com sucesso")
        return redirect("login")
    
    return render(request, "cadastro.html")