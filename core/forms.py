from django import forms
from .models import Produto, Fornecedor, Deposito, Movimentacao


class OrgForm(forms.ModelForm):
    def __init__(self, *args, org, **kwargs):
        super().__init__(*args, **kwargs)
        self.org = org
        self.instance.organizacao = org
        for campo, model in [('fornecedor', Fornecedor), ('produto', Produto), ('deposito', Deposito)]:
            if campo in self.fields:
                self.fields[campo].queryset = model.objects.filter(organizacao=org)


class ProdutoForm(OrgForm):
    def clean_quantidade_minima(self):
        valor = self.cleaned_data['quantidade_minima']
        if valor < 0:
            raise forms.ValidationError('O mínimo não pode ser negativo.')
        return valor

    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'categoria',
            'quantidade_minima',
            'fornecedor'
        ]

        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'quantidade_minima': 'Quantidade mínima',
            'fornecedor': 'Fornecedor'
        }


class FornecedorForm(OrgForm):
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


class DepositoForm(OrgForm):
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


class MovimentacaoForm(OrgForm):
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

class PeriodoForm(forms.Form):
    inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d'))
    fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d'))

    def clean(self):
        dados = super().clean()
        if dados.get('inicio') and dados.get('fim') and dados['inicio'] > dados['fim']:
            raise forms.ValidationError('A data inicial deve ser anterior ou igual à final.')
        return dados
