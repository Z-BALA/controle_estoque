from django.urls import path
from . import views


urlpatterns = [

    # Página inicial
    path(
        '',
        views.inicio,
        name='inicio'
    ),

    # Produtos
    path(
        'produtos/',
        views.produtos,
        name='produtos'
    ),

    path(
        'produtos/novo/',
        views.cadastrar_produto,
        name='cadastrar_produto'
    ),

    path(
        'produtos/editar/<int:id>/',
        views.editar_produto,
        name='editar_produto'
    ),

    path(
        'produtos/excluir/<int:id>/',
        views.excluir_produto,
        name='excluir_produto'
    ),

    # Fornecedores
    path(
        'fornecedores/',
        views.fornecedores,
        name='fornecedores'
    ),

    path(
        'fornecedores/novo/',
        views.cadastrar_fornecedor,
        name='cadastrar_fornecedor'
    ),

    path(
        'fornecedores/editar/<int:id>/',
        views.editar_fornecedor,
        name='editar_fornecedor'
    ),

    path(
        'fornecedores/excluir/<int:id>/',
        views.excluir_fornecedor,
        name='excluir_fornecedor'
    ),

    # Depósitos
    path(
        'depositos/',
        views.depositos,
        name='depositos'
    ),

    path(
        'depositos/novo/',
        views.cadastrar_deposito,
        name='cadastrar_deposito'
    ),

    path(
        'depositos/editar/<int:id>/',
        views.editar_deposito,
        name='editar_deposito'
    ),

    path(
        'depositos/excluir/<int:id>/',
        views.excluir_deposito,
        name='excluir_deposito'
    ),

    # Movimentações
    path(
        'movimentacoes/',
        views.movimentacoes,
        name='movimentacoes'
    ),

    path(
        'movimentacoes/novo/',
        views.cadastrar_movimentacao,
        name='cadastrar_movimentacao'
    ),

    # Estoque
    path(
        'estoque/',
        views.estoque,
        name='estoque'
    ),
]