from django.db import models

from Hacienda.models import Lote

# Create your models here.
class Dataset(models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True)
    Total_E1 = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Total_E2 = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Total_E3 = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Total_E4 = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Total_E5 = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Plantas = models.IntegerField(default=0, null=True, blank=True)
    Evapotranspiration_Crop = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Nvdi = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Relat_Hum_Max_Temp = models.DecimalField(max_digits=18, decimal_places=14)
    Temp_Air_Max = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Temp_Air_Min = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Dew_Temp_Max = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Precipitacion = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    Sunshine_Duration = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    hectareas = models.DecimalField(default=0,max_digits=7, decimal_places=4,)
    qq = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    edad = models.IntegerField(default=0)
    grade_monilla = models.IntegerField(default=0)
    date = models.DateTimeField(null=True)
    lost = models.DecimalField(max_digits=18, decimal_places=14, default=0.0)
    FechaRegistro = models.DateTimeField(auto_created=True,blank=True, null=True)
    
class HistorialPredict(models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=False)
    Qq = models.DecimalField(max_digits=8, decimal_places=4, null=False)
    Fecha = models.DateField(null=False)
    FechaRegistro = models.DateTimeField(auto_now_add=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)
