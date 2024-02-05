from datetime import datetime, timedelta
from enum import Enum
from django.db import models
import uuid

# Create your models here.


class Hacienda(models.Model):
    codigo = models.CharField(max_length=10)
    Nombre = models.CharField(max_length=40)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)
    def __str__(self):
        return self.Nombre


class Proyecto(models.Model):
    # campo_fk = models.ForeignKey(ModeloPrincipal, on_delete=models.CASCADE, null=True)
    Id_Hacienda = models.ForeignKey(Hacienda, on_delete=models.CASCADE, null=True)
    Codigo_Proyecto = models.CharField(max_length=10)
    Nombre = models.CharField(max_length=40)
    Densidad = models.IntegerField(null=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)


class Lote(models.Model):
    Id_Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    Codigo_Lote = models.CharField(max_length=10)
    Nombre = models.CharField(max_length=40)
    Variedad = models.CharField(max_length=20, null=True)
    Hectareas = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)
    FechaSiembra = models.DateTimeField(null=True)
    Edad =  models.IntegerField(null=True)

class Planta(models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True)
    Codigo_Planta = models.CharField(max_length=20) 
    Nombre = models.CharField(max_length=40) 
    Circunferencia = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    Activo = models.BooleanField(default=True)
    lat = models.DecimalField(max_digits=18, decimal_places=16, null=False)
    lng = models.DecimalField(max_digits=19, decimal_places=16, null=False)
    VisibleToStudent = models.BooleanField(null=False,default=True)


class Poligono (models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True)
    FillColor = models.CharField(max_length=7)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)


class GeoCoordenadas(models.Model):
    Id_Poligono = models.ForeignKey(Poligono, on_delete=models.CASCADE, null=True)
    lat = models.DecimalField(max_digits=18, decimal_places=16, null=False)
    lng = models.DecimalField(max_digits=19, decimal_places=16, null=False)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)


class Lectura(models.Model):
    Id_Planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True)
    E1 = models.IntegerField(default=0, blank=True, null=True)
    E2 = models.IntegerField(default=0, blank=True, null=True)
    E3 = models.IntegerField(default=0, blank=True, null=True)
    E4 = models.IntegerField(default=0, blank=True, null=True)
    E5 = models.IntegerField(default=0, blank=True, null=True)
    GR1 = models.IntegerField(default=0, blank=True, null=True)
    GR2 = models.IntegerField(default=0, blank=True, null=True)
    GR3 = models.IntegerField(default=0, blank=True, null=True)
    GR4 = models.IntegerField(default=0, blank=True, null=True)
    GR5 = models.IntegerField(default=0, blank=True, null=True)
    Monilla = models.IntegerField(default=0, blank=True, null=True)
    Total = models.IntegerField(default=0, blank=True, null=True)
    Cherelles = models.IntegerField(default=0, blank=True, null=True)
    Observacion = models.TextField(max_length=100, null=True, blank=True)
    FechaVisita = models.DateTimeField(null=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)
    GUIDLectura = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    SyncId = models.TextField(max_length=100, null=True)
    FechaRegistro = models.DateTimeField(auto_now_add=True)


class Produccion(models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=False)
    Qq = models.DecimalField(max_digits=8, decimal_places=4, null=False)
    Fecha = models.DateField(null=False)
    FechaRegistro = models.DateTimeField(auto_now_add=True)
    Activo = models.BooleanField(default=True)
    Usuario = models.TextField(default="Admin",max_length=100, null=True)
