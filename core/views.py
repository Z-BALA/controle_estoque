from .decorators import acesso, org_atual
from .services import registrar_movimentacao, linhas_estoque
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import (
    Produto,
    Fornecedor,
    Deposito,
    Movimentacao
)

from .forms import (
    ProdutoForm,
    FornecedorForm,
    DepositoForm,
    MovimentacaoForm
)


# =========================
# INÍCIO
# =========================

@acesso()
def inicio(request):
    org = org_atual(request)
    total_produtos = Produto.objects.filter(organizacao=org).count()
    total_fornecedores = Fornecedor.objects.filter(organizacao=org).count()
    total_depositos = Deposito.objects.filter(organizacao=org).count()
    total_movimentacoes = Movimentacao.objects.filter(organizacao=org).count()

    return render(
        request,
        'core/inicio.html',
        {
            'total_produtos': total_produtos,
            'total_fornecedores': total_fornecedores,
            'total_depositos': total_depositos,
            'total_movimentacoes': total_movimentacoes
        }
    )


# =========================
# PRODUTOS
# =========================

@acesso()
def produtos(request):
    org = org_atual(request)
    lista_produtos = Produto.objects.filter(organizacao=org).select_related("fornecedor")

    nome = request.GET.get('nome', '')
    categoria = request.GET.get('categoria', '')
    fornecedor = request.GET.get('fornecedor', '')
    fornecedores = Fornecedor.objects.filter(organizacao=org).order_by('nome')

    if nome:
        lista_produtos = lista_produtos.filter(nome__icontains=nome)
    if categoria:
        lista_produtos = lista_produtos.filter(categoria=categoria)
    if fornecedor:
        try:
            fornecedor_id = int(fornecedor)
        except ValueError:
            lista_produtos = lista_produtos.none()
        else:
            lista_produtos = lista_produtos.filter(fornecedor_id=fornecedor_id)

    return render(request, 'core/produtos.html', {
        'produtos': lista_produtos,
        'fornecedores': fornecedores,
        'categorias': Produto.CATEGORIAS,
        'nome_filtro': nome,
        'categoria_filtro': categoria,
        'fornecedor_filtro': fornecedor,
    })


@acesso(admin=True)
def cadastrar_produto(request):
    org = org_atual(request)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, org=org)

        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm(org=org)

    return render(
        request,
        'core/produto_form.html',
        {'form': form}
    )


@acesso(admin=True)
def editar_produto(request, id):
    org = org_atual(request)
    produto = get_object_or_404(Produto, id=id, organizacao=org)

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            org=org,
            instance=produto
        )

        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm(org=org, instance=produto)

    return render(
        request,
        'core/produto_form.html',
        {'form': form}
    )


@acesso(admin=True)
def excluir_produto(request, id):
    org = org_atual(request)
    produto = get_object_or_404(Produto, id=id, organizacao=org)

    if request.method == 'POST':
        produto.delete()
        return redirect('produtos')

    return render(
        request,
        'core/produto_confirmar_exclusao.html',
        {'produto': produto}
    )


# =========================
# FORNECEDORES
# =========================

@acesso()
def fornecedores(request):
    org = org_atual(request)
    lista_fornecedores = Fornecedor.objects.filter(organizacao=org)

    return render(
        request,
        'core/fornecedores.html',
        {'fornecedores': lista_fornecedores}
    )


@acesso(admin=True)
def cadastrar_fornecedor(request):
    org = org_atual(request)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, org=org)

        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    else:
        form = FornecedorForm(org=org)

    return render(
        request,
        'core/fornecedor_form.html',
        {'form': form}
    )


@acesso(admin=True)
def editar_fornecedor(request, id):
    org = org_atual(request)
    fornecedor = get_object_or_404(
        Fornecedor,
        id=id, organizacao=org
    )

    if request.method == 'POST':
        form = FornecedorForm(
            request.POST,
            org=org,
            instance=fornecedor
        )

        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    else:
        form = FornecedorForm(
            org=org,
            instance=fornecedor
        )

    return render(
        request,
        'core/fornecedor_form.html',
        {'form': form}
    )


@acesso(admin=True)
def excluir_fornecedor(request, id):
    org = org_atual(request)
    fornecedor = get_object_or_404(
        Fornecedor,
        id=id, organizacao=org
    )

    if request.method == 'POST':
        fornecedor.delete()
        return redirect('fornecedores')

    return render(
        request,
        'core/fornecedor_confirmar_exclusao.html',
        {'fornecedor': fornecedor}
    )


# =========================
# DEPÓSITOS
# =========================

@acesso()
def depositos(request):
    org = org_atual(request)
    lista_depositos = Deposito.objects.filter(organizacao=org)

    return render(
        request,
        'core/depositos.html',
        {'depositos': lista_depositos}
    )


@acesso(admin=True)
def cadastrar_deposito(request):
    org = org_atual(request)
    if request.method == 'POST':
        form = DepositoForm(request.POST, org=org)

        if form.is_valid():
            form.save()
            return redirect('depositos')
    else:
        form = DepositoForm(org=org)

    return render(
        request,
        'core/deposito_form.html',
        {'form': form}
    )


@acesso(admin=True)
def editar_deposito(request, id):
    org = org_atual(request)
    deposito = get_object_or_404(
        Deposito,
        id=id, organizacao=org
    )

    if request.method == 'POST':
        form = DepositoForm(
            request.POST,
            org=org,
            instance=deposito
        )

        if form.is_valid():
            form.save()
            return redirect('depositos')
    else:
        form = DepositoForm(
            org=org,
            instance=deposito
        )

    return render(
        request,
        'core/deposito_form.html',
        {'form': form}
    )


@acesso(admin=True)
def excluir_deposito(request, id):
    org = org_atual(request)
    deposito = get_object_or_404(
        Deposito,
        id=id, organizacao=org
    )

    if request.method == 'POST':
        deposito.delete()
        return redirect('depositos')

    return render(
        request,
        'core/deposito_confirmar_exclusao.html',
        {'deposito': deposito}
    )


# =========================
# MOVIMENTAÇÕES
# =========================

@acesso()
def movimentacoes(request):
    org = org_atual(request)
    lista_movimentacoes = Movimentacao.objects.filter(organizacao=org).select_related("produto", "deposito").order_by('-data')

    return render(
        request,
        'core/movimentacoes.html',
        {
            'movimentacoes': lista_movimentacoes
        }
    )


@acesso()
def cadastrar_movimentacao(request):
    org = org_atual(request)
    form = MovimentacaoForm(request.POST if request.method == 'POST' else None, org=org)
    if request.method == 'POST' and form.is_valid():
        try:
            registrar_movimentacao(org, **form.cleaned_data)
        except ValidationError as exc:
            form.add_error('quantidade', exc)
        else:
            return redirect('movimentacoes')
    return render(request, 'core/movimentacao_form.html', {'form':form})

@acesso()
def estoque(request):
    org = org_atual(request)
    return render(request, 'core/estoque.html', {'estoque':list(linhas_estoque(org))})

from .dashboard import periodo_validado, metricas
from django.http import HttpResponse, HttpResponseBadRequest
import csv

@acesso()
def dashboard(request):
    form, base = periodo_validado(request.GET, org_atual(request))
    contexto = metricas(base, request.user.perfil.eh_admin)
    contexto.update(form=form, mostra_series=request.user.perfil.eh_admin)
    return render(request, 'core/dashboard.html', contexto)

@acesso(admin=True)
def exportar_csv(request):
    form, base = periodo_validado(request.GET, org_atual(request))
    if not form.is_valid():
        return HttpResponseBadRequest('Período inválido.')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="movimentacoes.csv"'
    response.write('\ufeff')
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Data','Produto','Depósito','Tipo','Quantidade'])
    from django.utils.timezone import localtime
    def seguro(texto):
        return "'"+texto if texto.lstrip().startswith(('=','+','-','@','\t','\r')) else texto
    for m in base.select_related('produto','deposito').order_by('data'):
        writer.writerow([localtime(m.data).strftime('%d/%m/%Y %H:%M'),seguro(m.produto.nome),seguro(m.deposito.nome),m.get_tipo_display(),m.quantidade])
    return response
