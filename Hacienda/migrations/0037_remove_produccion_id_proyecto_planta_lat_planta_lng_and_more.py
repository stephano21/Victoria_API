# Generated by Django 4.2.1 on 2023-12-18 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hacienda', '0036_planta_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produccion',
            name='Id_Proyecto',
        ),
        migrations.AddField(
            model_name='planta',
            name='lat',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=18),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planta',
            name='lng',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produccion',
            name='Id_Lote',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Hacienda.lote'),
            preserve_default=False,
        ),
    ]
