from django.db.models import Sum, Q
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Produto, Deposito, Movimentacao

def saldo(org, produto, deposito):
    t = Movimentacao.objects.filter(organizacao=org, produto=produto, deposito=deposito).aggregate(entradas=Sum('quantidade', filter=Q(tipo='entrada')), saidas=Sum('quantidade', filter=Q(tipo='saida')))
    return (t['entradas'] or 0) - (t['saidas'] or 0)

def validar_movimentacao(org, produto, deposito, tipo, quantidade):
    if produto.organizacao_id != org.pk or deposito.organizacao_id != org.pk:
        raise ValidationError('Produto ou depósito de outra organização.')
    if quantidade <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')
    if tipo == 'saida' and quantidade > saldo(org, produto, deposito):
        raise ValidationError('Não há estoque suficiente neste depósito.')

@transaction.atomic
def registrar_movimentacao(org, **dados):
    dados['produto'] = Produto.objects.select_for_update().get(pk=dados['produto'].pk, organizacao=org)
    validar_movimentacao(org, **dados)
    return Movimentacao.objects.create(organizacao=org, **dados)

def linhas_estoque(org):
    totais = Movimentacao.objects.filter(organizacao=org).values('produto_id','deposito_id').annotate(entradas=Sum('quantidade', filter=Q(tipo='entrada')), saidas=Sum('quantidade', filter=Q(tipo='saida')))
    mapa = {(t['produto_id'], t['deposito_id']): t for t in totais}
    depositos = list(Deposito.objects.filter(organizacao=org))
    for produto in Produto.objects.filter(organizacao=org):
        for deposito in depositos:
            t = mapa.get((produto.pk,deposito.pk), {})
            e, s = t.get('entradas') or 0, t.get('saidas') or 0
            yield dict(produto=produto, deposito=deposito, entradas=e, saidas=s, saldo=e-s)
