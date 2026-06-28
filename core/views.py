from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def servicos(request):
    return render(request, 'servicos.html')

def contato(request):
    return render(request, 'contato.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'painel/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='/admin-santana/login/')
def admin_dashboard(request):
    return render(request, 'painel/dashboard.html')