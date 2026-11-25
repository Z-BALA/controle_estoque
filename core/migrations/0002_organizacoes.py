from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion as deletion

class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Organizacao', fields=[('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')), ('nome', models.CharField(max_length=120)), ('criada_em', models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name='Perfil', fields=[('id', models.BigAutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')), ('papel', models.CharField(max_length=10, choices=[('admin','Administrador'),('operador','Operador')], default='operador')), ('usuario', models.OneToOneField(on_delete=deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ('organizacao', models.ForeignKey(on_delete=deletion.PROTECT, to='core.organizacao'))]),
    ] + [migrations.AddField(model_name=n, name='organizacao', field=models.ForeignKey(null=True, on_delete=deletion.PROTECT, to='core.organizacao')) for n in ('produto','fornecedor','deposito','movimentacao')]
