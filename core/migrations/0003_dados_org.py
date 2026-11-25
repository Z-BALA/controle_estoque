from django.db import migrations
from django.conf import settings

def preencher(apps, schema_editor):
    org = apps.get_model('core','Organizacao').objects.create(nome='Organização padrão')
    for nome in ('Produto','Fornecedor','Deposito','Movimentacao'):
        apps.get_model('core',nome).objects.filter(organizacao__isnull=True).update(organizacao=org)
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Perfil = apps.get_model('core','Perfil')
    for user in User.objects.all():
        Perfil.objects.get_or_create(usuario=user, defaults={'organizacao':org,'papel':'admin' if user.is_superuser else 'operador'})

class Migration(migrations.Migration):
    dependencies = [('core','0002_organizacoes')]
    operations = [migrations.RunPython(preencher, migrations.RunPython.noop)]
