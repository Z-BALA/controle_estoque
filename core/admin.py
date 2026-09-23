from django.contrib import admin
from .models import Fornecedor, Produto, Deposito, Movimentacao


admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Deposito)
admin.site.register(Movimentacao)