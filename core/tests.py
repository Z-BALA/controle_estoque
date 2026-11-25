from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from .models import Organizacao, Perfil, Produto, Fornecedor, Deposito, Movimentacao
from .services import registrar_movimentacao

class P2Test(TestCase):
    def setUp(self):
        self.a = Organizacao.objects.create(nome='Empresa A')
        self.b = Organizacao.objects.create(nome='Empresa B')
        self.admin = get_user_model().objects.create_user('gestor')
        self.operador = get_user_model().objects.create_user('operador')
        self.user_b = get_user_model().objects.create_user('gestor_b')
        for u,o,p in [(self.admin,self.a,'admin'),(self.operador,self.a,'operador'),(self.user_b,self.b,'admin')]:
            Perfil.objects.create(usuario=u,organizacao=o,papel=p)
        self.fa = Fornecedor.objects.create(organizacao=self.a,nome='Fornecedor A',telefone='123')
        self.fb = Fornecedor.objects.create(organizacao=self.b,nome='Fornecedor B',telefone='123')
        self.pa = Produto.objects.create(organizacao=self.a,nome='Produto A',fornecedor=self.fa)
        self.pb = Produto.objects.create(organizacao=self.b,nome='Produto B',fornecedor=self.fb)
        self.da = Deposito.objects.create(organizacao=self.a,nome='Depósito A',endereco='Rua A')
        self.db = Deposito.objects.create(organizacao=self.b,nome='Depósito B',endereco='Rua B')
        self.ma = registrar_movimentacao(self.a,produto=self.pa,deposito=self.da,tipo='entrada',quantidade=10)
        registrar_movimentacao(self.a,produto=self.pa,deposito=self.da,tipo='saida',quantidade=3)
        registrar_movimentacao(self.b,produto=self.pb,deposito=self.db,tipo='entrada',quantidade=50)
        self.client.force_login(self.admin)
        self.api = APIClient(); self.api.force_authenticate(self.admin)
    def test_lista_isolada(self):
        r = self.client.get(reverse('produtos')); self.assertContains(r,'Produto A'); self.assertNotContains(r,'Produto B')
    def test_id_outra_empresa(self):
        self.assertEqual(self.client.get(reverse('editar_produto',args=[self.pb.pk])).status_code,404)
        self.assertEqual(self.api.get(f'/api/produtos/{self.pb.pk}/').status_code,404)
    def test_formulario_filtrado(self):
        r = self.client.get(reverse('cadastrar_produto'))
        self.assertEqual(list(r.context['form'].fields['fornecedor'].queryset),[self.fa])
        r = self.client.post(reverse('cadastrar_produto'),dict(nome='Inválido',quantidade_minima=0,fornecedor=self.fb.pk))
        self.assertEqual(r.status_code,200); self.assertFalse(Produto.objects.filter(nome='Inválido').exists())
    def test_criacao_api_organizacao(self):
        r = self.api.post('/api/produtos/',dict(nome='Novo',quantidade_minima=0,fornecedor=self.fa.pk,organizacao=self.b.pk),format='json')
        self.assertEqual(r.status_code,201); self.assertEqual(Produto.objects.get(nome='Novo').organizacao,self.a)
    def test_api_relacao_indevida(self):
        r = self.api.post('/api/produtos/',dict(nome='Inválido',fornecedor=self.fb.pk),format='json'); self.assertEqual(r.status_code,400)
    def test_saldo_insuficiente(self):
        r = self.api.post('/api/movimentacoes/',dict(produto=self.pa.pk,deposito=self.da.pk,tipo='saida',quantidade=8),format='json')
        self.assertEqual(r.status_code,400); self.assertEqual(Movimentacao.objects.filter(organizacao=self.a).count(),2)
    def test_dashboard_total_org(self):
        r = self.client.get('/dashboard/'); self.assertEqual(r.context['kpis']['total'],2); self.assertEqual(r.context['kpis']['entradas'],10); self.assertEqual(r.context['ranking'][0]['total'],3)
        self.assertEqual(self.api.get('/api/dashboard/').data['kpis']['total'],2)
    def test_dashboard_periodo(self):
        Movimentacao.objects.filter(pk=self.ma.pk).update(data=timezone.now()-timedelta(days=10))
        hoje = timezone.localdate().isoformat(); r = self.client.get('/dashboard/',{'inicio':hoje,'fim':hoje}); self.assertEqual(r.context['kpis']['total'],1)
    def test_dashboard_vazio_e_data_invalida(self):
        r=self.client.get('/dashboard/',{'inicio':'2099-01-01'}); self.assertEqual(r.context['kpis']['total'],0)
        self.assertEqual(self.api.get('/api/dashboard/?inicio=abc').status_code,400)
    def test_operador(self):
        self.client.force_login(self.operador); self.api.force_authenticate(self.operador)
        self.assertEqual(self.client.get(reverse('cadastrar_produto')).status_code,403)
        self.assertEqual(self.client.get('/dashboard/exportar/').status_code,403)
        self.assertNotIn('series',self.api.get('/api/dashboard/').data)
        self.assertEqual(self.api.post('/api/produtos/',{},format='json').status_code,403)
        self.assertEqual(self.api.post('/api/movimentacoes/',dict(produto=self.pa.pk,deposito=self.da.pk,tipo='saida',quantidade=1),format='json').status_code,201)
    def test_csv_isolado(self):
        r=self.client.get('/dashboard/exportar/'); self.assertContains(r,'Produto A'); self.assertNotContains(r,'Produto B')
    def test_anonimo(self):
        self.client.logout(); self.api.force_authenticate(None)
        self.assertEqual(self.client.get('/').status_code,302)
        self.assertIn(self.api.get('/api/produtos/').status_code,[401,403])

    def test_busca_produtos_com_filtros_da_p1(self):
        self.pa.categoria = 'INF'
        self.pa.save(update_fields=['categoria'])
        url = reverse('produtos')
        response = self.client.get(url, {'nome': 'produto', 'categoria': 'INF', 'fornecedor': self.fa.pk})
        self.assertEqual(list(response.context['produtos']), [self.pa])
        self.assertEqual(list(response.context['fornecedores']), [self.fa])

        for filtros in ({'nome': 'Produto B'}, {'categoria': 'ELE'}, {'fornecedor': self.fb.pk}, {'fornecedor': 'invalido'}):
            response = self.client.get(url, filtros)
            self.assertEqual(list(response.context['produtos']), [])
