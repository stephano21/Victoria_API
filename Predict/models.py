from django.db import models

from Hacienda.models import Lote

# Create your models here.
class Dataset(models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True)
    edad = models.IntegerField(default=0, null=True, blank=True)
    E1 = models.IntegerField(default=0, null=True, blank=True)
    E2 = models.IntegerField(default=0, null=True, blank=True)
    E3 = models.IntegerField(default=0, null=True, blank=True)
    E4 = models.IntegerField(default=0, null=True, blank=True)
    E5 = models.IntegerField(default=0, null=True, blank=True)
    grade_monilla = models.IntegerField(default=0, null=True, blank=True)
    qq = models.DecimalField(max_digits=18, decimal_places=3)
    Evapotranspiration_Crop = models.DecimalField(max_digits=18, decimal_places=3)
    Nvdi = models.DecimalField(max_digits=18, decimal_places=3)
    Relat_Hum_Max_Temp = models.DecimalField(max_digits=18, decimal_places=3)
    Temp_Air_Max = models.DecimalField(max_digits=18, decimal_places=3)
    Temp_Air_Min = models.DecimalField(max_digits=18, decimal_places=3)
    Dew_Temp_Max = models.DecimalField(max_digits=18, decimal_places=3)
    Precipitacion = models.DecimalField(max_digits=18, decimal_places=3)
    Sunshine_Duration = models.DecimalField(max_digits=18, decimal_places=3)
    date = models.DateTimeField(null=True)
    