# Generated by Django 4.2.1 on 2024-01-31 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hacienda', '0040_lote_edad'),
        ('Users', '0003_perfil_id_hacienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='Id_Hacienda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Hacienda.hacienda'),
        ),
    ]