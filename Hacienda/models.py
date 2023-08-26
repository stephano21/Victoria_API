from enum import Enum
from django.db import models
# Create your models here.

class Hacienda(models.Model): 
    codigo = models.CharField(max_length=10) 
    Nombre = models.CharField(max_length=40)
    Activo = models.BooleanField(default=True)


class Proyecto(models.Model): 
    #campo_fk = models.ForeignKey(ModeloPrincipal, on_delete=models.CASCADE, null=True) 
    Id_Hacienda = models.ForeignKey(Hacienda, on_delete=models.CASCADE, null=True) 
    Codigo_Proyecto = models.CharField(max_length=10) 
    Nombre = models.CharField(max_length=40)
    Activo = models.BooleanField(default=True)

    
class Lote(models.Model): 
    Id_Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True) 
    Codigo_Lote = models.CharField(max_length=10) 
    Nombre = models.CharField(max_length=40) 
    Variedad = models.CharField(max_length=20, null=True) 
    Hectareas = models.IntegerField( null=True)
    Activo = models.BooleanField(default=True)

class Poligono (models.Model):
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True)
    FillColor = models.CharField(max_length=7)
    Activo = models.BooleanField(default=True)


class GeoCoordenadas(models.Model):
    Id_Poligono = models.ForeignKey(Poligono, on_delete=models.CASCADE, null=True)
    lat = models.DecimalField(max_digits=18, decimal_places=16, null=False)
    lng = models.DecimalField(max_digits=19, decimal_places=16, null=False)
    Activo = models.BooleanField(default=True)
""" class Estacion(models.Model): 
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True) 
    Codigo_Estacion = models.CharField(max_length=20) 
    Nombre = models.CharField(max_length=40)
    Activo = models.BooleanField(default=True)


class Planta(models.Model): 
    Id_Estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True) 
    Codigo_Planta = models.CharField(max_length=20) 
    Nombre = models.CharField(max_length=40) 
    Activo = models.BooleanField(default=True) """

class EnumMonilla(models.IntegerChoices):
    Grado1 = 1
    Grado2 = 2
    Grado3 = 3
    Grado4 = 4
    Grado5 = 5   

class Lectura(models.Model): 
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True) 
    E1 = models.IntegerField(default=0, blank=True, null=True)
    E2 = models.IntegerField(default=0, blank=True, null=True)
    E3 = models.IntegerField(default=0, blank=True, null=True)
    E4 = models.IntegerField(default=0, blank=True, null=True)
    E5 = models.IntegerField(default=0, blank=True, null=True)
    Monilla = models.IntegerField(choices=EnumMonilla.choices)
    Phythptora = models.IntegerField(default=0, blank=True, null=True)
    Colletotrichum = models.IntegerField(default=0, blank=True, null=True)
    Corynespora = models.IntegerField(default=0, blank=True, null=True)
    Lasodiplodia = models.IntegerField(default=0, blank=True, null=True)
    Cherelles = models.IntegerField(default=0, blank=True, null=True)
    Insectos = models.IntegerField(default=0, blank=True, null=True)
    Animales = models.IntegerField(default=0, blank=True, null=True)
    Observacion = models.TextField(max_length=100, null=True)
    FechaVisita = models.DateField(null=True)
    Activo = models.BooleanField(default=True)


