from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} — {self.placa}'
    

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_estimada = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('andamento', 'Em andamento'),
        ('aguardando', 'Aguardando peças'),
        ('finalizada', 'Finalizada'),
        ('entregue', 'Entregue'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordens')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='ordens')
    km_atual = models.IntegerField(blank=True, null=True)
    defeito_relatado = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    previsao_entrega = models.DateField(blank=True, null=True)
    atendente = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OS #{self.id} — {self.cliente.nome}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())


class ItemOrdemServico(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.servico.nome} (x{self.quantidade})'