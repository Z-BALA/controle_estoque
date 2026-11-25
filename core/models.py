from django.db import models
from django.conf import settings


class Organizacao(models.Model):
    nome = models.CharField(max_length=120)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.PROTECT)
    papel = models.CharField(max_length=10, choices=[("admin", "Administrador"), ("operador", "Operador")], default="operador")

    @property
    def eh_admin(self):
        return self.papel == "admin"

    def __str__(self):
        return str(self.usuario)


class DaOrganizacao(models.Model):
    organizacao = models.ForeignKey(Organizacao, on_delete=models.PROTECT)

    class Meta:
        abstract = True



class Fornecedor(DaOrganizacao):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome


class Produto(DaOrganizacao):

    CATEGORIAS = [
        ('INF', 'Informática'),
        ('ELE', 'Eletrônicos'),
        ('ESC', 'Material de Escritório'),
        ('LIM', 'Material de Limpeza'),
        ('FER', 'Ferramentas'),
        ('EPI', 'Equipamentos de Proteção'),
        ('MOV', 'Móveis'),
        ('OUT', 'Outros'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade_minima = models.IntegerField(default=0)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default="OUT")
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome


class Deposito(DaOrganizacao):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Movimentacao(DaOrganizacao):
    ENTRADA = 'entrada'
    SAIDA = 'saida'

    TIPOS = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )
    deposito = models.ForeignKey(
        Deposito,
        on_delete=models.CASCADE
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto} - {self.tipo} - {self.quantidade}'