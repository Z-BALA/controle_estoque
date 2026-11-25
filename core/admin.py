from django.contrib import admin
from .models import Organizacao, Perfil, Fornecedor, Produto, Deposito, Movimentacao

admin.site.has_permission = lambda request: request.user.is_active and request.user.is_superuser
admin.site.register(Organizacao)
admin.site.register(Perfil)

class ConsultaNegocio(admin.ModelAdmin):
    list_filter = ('organizacao',)
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

for model in (Fornecedor, Produto, Deposito, Movimentacao):
    admin.site.register(model, ConsultaNegocio)
