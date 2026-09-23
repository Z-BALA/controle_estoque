from django import forms
from django.db.models import Sum

from .models import (
    Produto,
    Fornecedor,
    Deposito,
    Movimentacao
)


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'quantidade_minima',
            'categoria',
            'fornecedor'
        ]

        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'quantidade_minima': 'Quantidade mínima',
            'categoria': 'Categoria',
            'fornecedor': 'Fornecedor'
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'nome',
            'telefone',
            'email'
        ]

        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'E-mail'
        }


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = [
            'nome',
            'endereco'
        ]

        labels = {
            'nome': 'Nome',
            'endereco': 'Endereço'
        }


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'produto',
            'deposito',
            'tipo',
            'quantidade'
        ]

        labels = {
            'produto': 'Produto',
            'deposito': 'Depósito',
            'tipo': 'Tipo de movimentação',
            'quantidade': 'Quantidade'
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']

        if quantidade <= 0:
            raise forms.ValidationError(
                'A quantidade deve ser maior que zero.'
            )

        return quantidade

    def clean(self):
        dados = super().clean()

        produto = dados.get('produto')
        deposito = dados.get('deposito')
        tipo = dados.get('tipo')
        quantidade = dados.get('quantidade')

        if not produto or not deposito or not tipo or not quantidade:
            return dados

        if tipo == Movimentacao.SAIDA:

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

            estoque_atual = entradas - saidas

            if quantidade > estoque_atual:
                raise forms.ValidationError(
                    f'Não há estoque suficiente neste depósito. '
                    f'Estoque atual: {estoque_atual}.'
                )

        return dados