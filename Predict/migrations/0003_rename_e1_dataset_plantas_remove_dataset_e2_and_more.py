# Generated by Django 4.2.1 on 2024-02-19 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predict', '0002_dataset_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='E1',
            new_name='Plantas',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='E2',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='E3',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='E4',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='E5',
        ),
        migrations.AddField(
            model_name='dataset',
            name='FechaRegistro',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Total_E1',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Total_E2',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Total_E3',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Total_E4',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='dataset',
            name='Total_E5',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='dataset',
            name='hectareas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='lost',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Dew_Temp_Max',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Evapotranspiration_Crop',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Nvdi',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Precipitacion',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Sunshine_Duration',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Temp_Air_Max',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='Temp_Air_Min',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='edad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='grade_monilla',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='qq',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=18),
        ),
    ]