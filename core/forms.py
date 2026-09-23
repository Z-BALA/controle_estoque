from django import forms
from .models import Produto, Fornecedor, Deposito, Movimentacao


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'quantidade_minima',
            'fornecedor'
        ]

        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'quantidade_minima': 'Quantidade mínima',
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