from pyexpat import model
from django.db import models

from Hacienda.models import Hacienda

# Create your models here.


class Daily_Indicadores(models.Model):
    # Date info
    Id_Hacienda = models.ForeignKey(
        Hacienda, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateTimeField(blank=True, null=True)
    Date_Arable_Sync = models.DateTimeField(blank=True, null=True)
    Date_Sync = models.DateTimeField(auto_created=True, blank=True, null=True)
    # Location Info
    Lat = models.DecimalField(max_digits=18, decimal_places=16, null=True)
    Lng = models.DecimalField(max_digits=18, decimal_places=16, null=True)
    LocationID = models.CharField(null=True)
    # device
    Device = models.CharField(null=False)
    # Precipitation
    Precipitacion = models.DecimalField(
        max_digits=18, decimal_places=16, null=True)
    Precipitacion_Hours = models.IntegerField(null=True)
    # Temp Air
    Temp_Air_Mean = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Temp_Air_Min = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Temp_Air_Max = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Temp_Air_Max_Day = models.DateTimeField(blank=True, null=True)
    Temp_Air_Min_Day = models.DateTimeField(blank=True, null=True)
    # Temperature Below
    Temp_Below = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    Temp_Below_Mean = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Dew Temp
    Dew_Temp_Mean = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Dew_Temp_Max = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Dew_Temp_At_Min_Temp = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Normalized Difference Vegetative Index
    Ndvi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # Evapotranspiration
    Evapotranspiration = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Evapotranspiration_Crop = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Relative Humidity
    Relat_Hum_Mean = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Relat_Hum_Min = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Relat_Hum_Max = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Relat_Hum_Max_Temp = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Relat_Hum_Min_Temp = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Crop
    Crop_Water_Demand = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Sushine Duration
    Sunshine_Duration = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Daily Light Integral
    Dli = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # Sea Level Pressure
    Sea_Level_Pressure = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Vapor Pressure
    Vapor_Pressure = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Vapor_Pressure_Deficit = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    # Shortwave Downwelling
    Shortwave_Downwelling = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Arable", max_length=100, null=True)
