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

def inicio(request):
    total_produtos = Produto.objects.count()
    total_fornecedores = Fornecedor.objects.count()
    total_depositos = Deposito.objects.count()
    total_movimentacoes = Movimentacao.objects.count()

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

def produtos(request):
    lista_produtos = Produto.objects.all()

    return render(
        request,
        'core/produtos.html',
        {'produtos': lista_produtos}
    )


def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm()

    return render(
        request,
        'core/produto_form.html',
        {'form': form}
    )


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            instance=produto
        )

        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(
        request,
        'core/produto_form.html',
        {'form': form}
    )


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

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

def fornecedores(request):
    lista_fornecedores = Fornecedor.objects.all()

    return render(
        request,
        'core/fornecedores.html',
        {'fornecedores': lista_fornecedores}
    )


def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    else:
        form = FornecedorForm()

    return render(
        request,
        'core/fornecedor_form.html',
        {'form': form}
    )


def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(
        Fornecedor,
        id=id
    )

    if request.method == 'POST':
        form = FornecedorForm(
            request.POST,
            instance=fornecedor
        )

        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    else:
        form = FornecedorForm(
            instance=fornecedor
        )

    return render(
        request,
        'core/fornecedor_form.html',
        {'form': form}
    )


def excluir_fornecedor(request, id):
    fornecedor = get_object_or_404(
        Fornecedor,
        id=id
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

def depositos(request):
    lista_depositos = Deposito.objects.all()

    return render(
        request,
        'core/depositos.html',
        {'depositos': lista_depositos}
    )


def cadastrar_deposito(request):
    if request.method == 'POST':
        form = DepositoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('depositos')
    else:
        form = DepositoForm()

    return render(
        request,
        'core/deposito_form.html',
        {'form': form}
    )


def editar_deposito(request, id):
    deposito = get_object_or_404(
        Deposito,
        id=id
    )

    if request.method == 'POST':
        form = DepositoForm(
            request.POST,
            instance=deposito
        )

        if form.is_valid():
            form.save()
            return redirect('depositos')
    else:
        form = DepositoForm(
            instance=deposito
        )

    return render(
        request,
        'core/deposito_form.html',
        {'form': form}
    )


def excluir_deposito(request, id):
    deposito = get_object_or_404(
        Deposito,
        id=id
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

def movimentacoes(request):
    lista_movimentacoes = Movimentacao.objects.all().order_by('-data')

    return render(
        request,
        'core/movimentacoes.html',
        {
            'movimentacoes': lista_movimentacoes
        }
    )


def cadastrar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            movimentacao = form.save()

            # Verifica se é uma saída
            if movimentacao.tipo == Movimentacao.SAIDA:

                produto = movimentacao.produto
                deposito = movimentacao.deposito

                entradas = Movimentacao.objects.filter(
                    produto=produto,
                    deposito=deposito,
                    tipo=Movimentacao.ENTRADA
                ).aggregate(
                    total=Sum('quantidade')
                )['total'] or 0

                saidas = Movimentacao.objects.filter(
                    produto=produto,
                    deposito=deposito,
                    tipo=Movimentacao.SAIDA
                ).aggregate(
                    total=Sum('quantidade')
                )['total'] or 0

                saldo = entradas - saidas

                if saldo < 0:
                    movimentacao.delete()

                    form.add_error(
                        'quantidade',
                        'Não há estoque suficiente neste depósito.'
                    )

                else:
                    return redirect('movimentacoes')

            else:
                return redirect('movimentacoes')

    else:
        form = MovimentacaoForm()

    return render(
        request,
        'core/movimentacao_form.html',
        {'form': form}
    )


# =========================
# ESTOQUE
# =========================

def estoque(request):

    produtos = Produto.objects.all()
    depositos = Deposito.objects.all()

    estoque = []

    for produto in produtos:

        for deposito in depositos:

            entradas = Movimentacao.objects.filter(
                produto=produto,
                deposito=deposito,
                tipo=Movimentacao.ENTRADA
            ).aggregate(
                total=Sum('quantidade')
            )['total'] or 0

            saidas = Movimentacao.objects.filter(
                produto=produto,
                deposito=deposito,
                tipo=Movimentacao.SAIDA
            ).aggregate(
                total=Sum('quantidade')
            )['total'] or 0

            saldo = entradas - saidas

            estoque.append({
                'produto': produto,
                'deposito': deposito,
                'entradas': entradas,
                'saidas': saidas,
                'saldo': saldo
            })

    return render(
        request,
        'core/estoque.html',
        {'estoque': estoque}
    )