from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProdutoAPI, FornecedorAPI, DepositoAPI, MovimentacaoAPI, EstoqueAPI, DashboardAPI
router = DefaultRouter()
router.register('produtos', ProdutoAPI)
router.register('fornecedores', FornecedorAPI)
router.register('depositos', DepositoAPI)
router.register('movimentacoes', MovimentacaoAPI)
urlpatterns = [path('',include(router.urls)),path('estoque/',EstoqueAPI.as_view()),path('dashboard/',DashboardAPI.as_view())]
