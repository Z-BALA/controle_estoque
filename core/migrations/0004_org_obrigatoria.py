from django.db import migrations, models
import django.db.models.deletion as deletion

class Migration(migrations.Migration):
    dependencies = [('core','0003_dados_org')]
    operations = [migrations.AlterField(model_name=n, name='organizacao', field=models.ForeignKey(on_delete=deletion.PROTECT, to='core.organizacao')) for n in ('produto','fornecedor','deposito','movimentacao')]
