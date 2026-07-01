from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cliente, Veiculo, Servico, OrdemServico, ItemOrdemServico
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa
import io

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


# ============================================================
# SERVIÇOS (ADMIN)
# ============================================================

@login_required(login_url='/admin-santana/login/')
def servicos_admin_lista(request):
    pesquisa = request.GET.get('q', '')
    servicos_admin = Servico.objects.filter(nome__icontains=pesquisa) if pesquisa else Servico.objects.all()
    return render(request, 'painel/servicos/lista.html', {'servicos_admin': servicos_admin, 'pesquisa': pesquisa})

@login_required(login_url='/admin-santana/login/')
def servico_novo(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST.get('descricao', '')
        preco = request.POST['preco']
        duracao_estimada = request.POST.get('duracao_estimada', '')
        Servico.objects.create(nome=nome, descricao=descricao, preco=preco, duracao_estimada=duracao_estimada)
        messages.success(request, 'Serviço cadastrado com sucesso!')
        return redirect('servicos_admin_lista')
    return render(request, 'painel/servicos/form.html', {'acao': 'Novo'})

@login_required(login_url='/admin-santana/login/')
def servico_editar(request, id):
    servico = get_object_or_404(Servico, id=id)
    if request.method == 'POST':
        servico.nome = request.POST['nome']
        servico.descricao = request.POST.get('descricao', '')
        servico.preco = request.POST['preco']
        servico.duracao_estimada = request.POST.get('duracao_estimada', '')
        servico.save()
        messages.success(request, 'Serviço atualizado com sucesso!')
        return redirect('servicos_admin_lista')
    return render(request, 'painel/servicos/form.html', {'acao': 'Editar', 'servico': servico})

@login_required(login_url='/admin-santana/login/')
def servico_excluir(request, id):
    servico = get_object_or_404(Servico, id=id)
    servico.delete()
    messages.success(request, 'Serviço excluído com sucesso!')
    return redirect('servicos_admin_lista')


# ============================================================
# ORDEM DE SERVIÇO
# ============================================================

@login_required(login_url='/admin-santana/login/')
def ordens_lista(request):
    pesquisa = request.GET.get('q', '')
    if pesquisa:
        ordens = OrdemServico.objects.filter(cliente__nome__icontains=pesquisa)
    else:
        ordens = OrdemServico.objects.all()
    ordens = ordens.order_by('-criado_em')
    return render(request, 'painel/ordens/lista.html', {'ordens': ordens, 'pesquisa': pesquisa})


@login_required(login_url='/admin-santana/login/')
def ordem_nova(request):
    clientes = Cliente.objects.all()
    servicos_disponiveis = Servico.objects.all()

    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        veiculo = get_object_or_404(Veiculo, id=request.POST['veiculo'])

        ordem = OrdemServico.objects.create(
            cliente=cliente,
            veiculo=veiculo,
            km_atual=request.POST.get('km_atual') or None,
            defeito_relatado=request.POST.get('defeito_relatado', ''),
            status=request.POST.get('status', 'aberta'),
            previsao_entrega=request.POST.get('previsao_entrega') or None,
            atendente=request.POST.get('atendente', ''),
            observacoes=request.POST.get('observacoes', ''),
        )

        servicos_ids = request.POST.getlist('servico_id[]')
        quantidades = request.POST.getlist('quantidade[]')
        precos = request.POST.getlist('preco_unitario[]')

        for sid, qtd, preco in zip(servicos_ids, quantidades, precos):
            if sid:
                ItemOrdemServico.objects.create(
                    ordem=ordem,
                    servico_id=sid,
                    quantidade=qtd,
                    preco_unitario=preco,
                )

        messages.success(request, 'Ordem de Serviço criada com sucesso!')
        return redirect('ordens_lista')

    return render(request, 'painel/ordens/form.html', {
        'acao': 'Nova',
        'clientes': clientes,
        'servicos_disponiveis': servicos_disponiveis,
    })


@login_required(login_url='/admin-santana/login/')
def ordem_editar(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    servicos_disponiveis = Servico.objects.all()
    veiculos_do_cliente = Veiculo.objects.filter(cliente=ordem.cliente)

    if request.method == 'POST':
        ordem.cliente = get_object_or_404(Cliente, id=request.POST['cliente'])
        ordem.veiculo = get_object_or_404(Veiculo, id=request.POST['veiculo'])
        ordem.km_atual = request.POST.get('km_atual') or None
        ordem.defeito_relatado = request.POST.get('defeito_relatado', '')
        ordem.status = request.POST.get('status', 'aberta')
        ordem.previsao_entrega = request.POST.get('previsao_entrega') or None
        ordem.atendente = request.POST.get('atendente', '')
        ordem.observacoes = request.POST.get('observacoes', '')
        ordem.save()

        ordem.itens.all().delete()
        servicos_ids = request.POST.getlist('servico_id[]')
        quantidades = request.POST.getlist('quantidade[]')
        precos = request.POST.getlist('preco_unitario[]')

        for sid, qtd, preco in zip(servicos_ids, quantidades, precos):
            if sid:
                ItemOrdemServico.objects.create(
                    ordem=ordem,
                    servico_id=sid,
                    quantidade=qtd,
                    preco_unitario=preco,
                )

        messages.success(request, 'Ordem de Serviço atualizada com sucesso!')
        return redirect('ordens_lista')

    return render(request, 'painel/ordens/form.html', {
        'acao': 'Editar',
        'ordem': ordem,
        'clientes': clientes,
        'servicos_disponiveis': servicos_disponiveis,
        'veiculos_do_cliente': veiculos_do_cliente,
    })


@login_required(login_url='/admin-santana/login/')
def ordem_excluir(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    ordem.delete()
    messages.success(request, 'Ordem de Serviço excluída com sucesso!')
    return redirect('ordens_lista')


@login_required(login_url='/admin-santana/login/')
def ordem_visualizar(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    return render(request, 'painel/ordens/visualizar.html', {'ordem': ordem})


@login_required(login_url='/admin-santana/login/')
def ordem_pdf(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    html_string = render_to_string('painel/ordens/pdf.html', {'ordem': ordem})

    resultado = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_string.encode('UTF-8')), resultado)

    if pdf.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    response = HttpResponse(resultado.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS_{ordem.id}_{ordem.cliente.nome}.pdf"'
    return response

@login_required(login_url='/admin-santana/login/')
def api_veiculos_cliente(request, cliente_id):
    veiculos = Veiculo.objects.filter(cliente_id=cliente_id).values('id', 'marca', 'modelo', 'placa')
    return JsonResponse(list(veiculos), safe=False)

@login_required(login_url='/admin-santana/login/')
@require_POST
def ordem_atualizar_status(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    novo_status = request.POST.get('status')
    if novo_status in dict(OrdemServico.STATUS_CHOICES):
        ordem.status = novo_status
        ordem.save()
        return JsonResponse({'sucesso': True})
    return JsonResponse({'sucesso': False}, status=400)