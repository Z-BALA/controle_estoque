from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from .forms import PeriodoForm
from .models import Movimentacao

def periodo_validado(params, org):
    form = PeriodoForm(params)
    base = Movimentacao.objects.filter(organizacao=org)
    if not form.is_valid():
        return form, base.none()
    for campo, lookup in [('inicio','data__date__gte'),('fim','data__date__lte')]:
        if form.cleaned_data.get(campo):
            base = base.filter(**{lookup:form.cleaned_data[campo]})
    return form, base

def metricas(base, admin):
    kpis = base.aggregate(total=Count('id'), entradas=Sum('quantidade',filter=Q(tipo='entrada')), saidas=Sum('quantidade',filter=Q(tipo='saida')), produtos=Count('produto',distinct=True))
    kpis = {k:v or 0 for k,v in kpis.items()}
    ranking = list(base.filter(tipo='saida').values('produto_id','produto__nome').annotate(total=Sum('quantidade')).order_by('-total','produto_id')[:5])
    distribuicao = list(base.values('tipo').annotate(total=Count('id')).order_by('tipo'))
    dados = dict(kpis=kpis, ranking=ranking, distribuicao=distribuicao)
    if admin:
        dados['series'] = [dict(mes=x['mes'].strftime('%m/%Y'), entradas=x['entradas'] or 0, saidas=x['saidas'] or 0) for x in base.annotate(mes=TruncMonth('data')).values('mes').annotate(entradas=Sum('quantidade',filter=Q(tipo='entrada')),saidas=Sum('quantidade',filter=Q(tipo='saida'))).order_by('mes')]
    return dados
