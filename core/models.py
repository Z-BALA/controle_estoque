from django.db import models


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade_minima = models.IntegerField(default=0)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome


class Deposito(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
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