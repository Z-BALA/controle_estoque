from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Produto, Fornecedor, Deposito, Movimentacao
from .serializers import ProdutoSerializer, FornecedorSerializer, DepositoSerializer, MovimentacaoSerializer
from .permissions import PermissaoOrganizacao
from .services import linhas_estoque
from .dashboard import metricas, periodo_validado
from rest_framework.exceptions import ValidationError

class Escopo:
    permission_classes = [PermissaoOrganizacao]
    def get_queryset(self):
        return self.queryset.filter(organizacao=self.request.user.perfil.organizacao)
    def perform_create(self, serializer):
        serializer.save(organizacao=self.request.user.perfil.organizacao)

class ProdutoAPI(Escopo, viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('fornecedor').order_by('id')
    serializer_class = ProdutoSerializer

class FornecedorAPI(Escopo, viewsets.ModelViewSet):
    queryset = Fornecedor.objects.order_by('id')
    serializer_class = FornecedorSerializer

class DepositoAPI(Escopo, viewsets.ModelViewSet):
    queryset = Deposito.objects.order_by('id')
    serializer_class = DepositoSerializer

class MovimentacaoAPI(Escopo, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Movimentacao.objects.select_related('produto','deposito').order_by('-data')
    serializer_class = MovimentacaoSerializer
    operador_cria = True

class EstoqueAPI(APIView):
    permission_classes = [PermissaoOrganizacao]
    def get(self, request):
        return Response([dict(produto=l['produto'].pk, deposito=l['deposito'].pk, entradas=l['entradas'], saidas=l['saidas'], saldo=l['saldo']) for l in linhas_estoque(request.user.perfil.organizacao)])

class DashboardAPI(APIView):
    permission_classes = [PermissaoOrganizacao]
    def get(self, request):
        form, base = periodo_validado(request.GET, request.user.perfil.organizacao)
        if not form.is_valid():
            raise ValidationError(form.errors.get_json_data())
        return Response(metricas(base, request.user.perfil.eh_admin))
