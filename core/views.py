from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Veiculo

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

# ============================================================
# CLIENTES
# ============================================================

@login_required(login_url='/admin-santana/login/')
def clientes_lista(request):
    pesquisa = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nome__icontains=pesquisa) if pesquisa else Cliente.objects.all()
    return render(request, 'painel/clientes/lista.html', {'clientes': clientes, 'pesquisa': pesquisa})

@login_required(login_url='/admin-santana/login/')
def cliente_novo(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        telefone = request.POST['telefone']
        email = request.POST.get('email', '')
        endereco = request.POST.get('endereco', '')
        Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone, email=email, endereco=endereco)
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('clientes_lista')
    return render(request, 'painel/clientes/form.html', {'acao': 'Novo'})

@login_required(login_url='/admin-santana/login/')
def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.cpf = request.POST['cpf']
        cliente.telefone = request.POST['telefone']
        cliente.email = request.POST.get('email', '')
        cliente.endereco = request.POST.get('endereco', '')
        cliente.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('clientes_lista')
    return render(request, 'painel/clientes/form.html', {'acao': 'Editar', 'cliente': cliente})

@login_required(login_url='/admin-santana/login/')
def cliente_excluir(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, 'Cliente excluído com sucesso!')
    return redirect('clientes_lista')

# ============================================================
# VEÍCULOS
# ============================================================

@login_required(login_url='/admin-santana/login/')
def veiculos_lista(request):
    pesquisa = request.GET.get('q', '')
    veiculos = Veiculo.objects.filter(placa__icontains=pesquisa) if pesquisa else Veiculo.objects.all()
    return render(request, 'painel/veiculos/lista.html', {'veiculos': veiculos, 'pesquisa': pesquisa})

@login_required(login_url='/admin-santana/login/')
def veiculo_novo(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        ano = request.POST['ano']
        placa = request.POST['placa']
        cor = request.POST.get('cor', '')
        Veiculo.objects.create(cliente=cliente, marca=marca, modelo=modelo, ano=ano, placa=placa, cor=cor)
        messages.success(request, 'Veículo cadastrado com sucesso!')
        return redirect('veiculos_lista')
    return render(request, 'painel/veiculos/form.html', {'acao': 'Novo', 'clientes': clientes})

@login_required(login_url='/admin-santana/login/')
def veiculo_editar(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        veiculo.cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        veiculo.marca = request.POST['marca']
        veiculo.modelo = request.POST['modelo']
        veiculo.ano = request.POST['ano']
        veiculo.placa = request.POST['placa']
        veiculo.cor = request.POST.get('cor', '')
        veiculo.save()
        messages.success(request, 'Veículo atualizado com sucesso!')
        return redirect('veiculos_lista')
    return render(request, 'painel/veiculos/form.html', {'acao': 'Editar', 'veiculo': veiculo, 'clientes': clientes})

@login_required(login_url='/admin-santana/login/')
def veiculo_excluir(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    veiculo.delete()
    messages.success(request, 'Veículo excluído com sucesso!')
    return redirect('veiculos_lista')