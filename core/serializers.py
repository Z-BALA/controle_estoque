from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Produto, Fornecedor, Deposito, Movimentacao
from .services import registrar_movimentacao, validar_movimentacao

class OrgSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        perfil = getattr(getattr(request, 'user', None), 'perfil', None)
        for name, model in [('fornecedor', Fornecedor), ('produto', Produto), ('deposito', Deposito)]:
            if name in self.fields:
                self.fields[name].queryset = model.objects.filter(organizacao=perfil.organizacao) if perfil else model.objects.none()

class ProdutoSerializer(OrgSerializer):
    quantidade_minima = serializers.IntegerField(min_value=0, required=False)
    class Meta:
        model = Produto
        fields = ['id','nome','descricao','categoria','quantidade_minima','fornecedor']

class FornecedorSerializer(OrgSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id','nome','telefone','email']

class DepositoSerializer(OrgSerializer):
    class Meta:
        model = Deposito
        fields = ['id','nome','endereco']

class MovimentacaoSerializer(OrgSerializer):
    quantidade = serializers.IntegerField(min_value=1)
    class Meta:
        model = Movimentacao
        fields = ['id','produto','deposito','tipo','quantidade','data']
        read_only_fields = ['data']

    def create(self, validated_data):
        org = validated_data.pop('organizacao')
        try:
            return registrar_movimentacao(org, **validated_data)
        except ValidationError as exc:
            raise serializers.ValidationError({'quantidade':exc.messages})
