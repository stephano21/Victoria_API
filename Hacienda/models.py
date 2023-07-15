from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Campos adicionales, si los necesitas
    # Por ejemplo:
    cedula = models.CharField(max_length=10) 
    # fecha_nacimiento = models.DateField(blank=True, null=True)

    # Campos heredados de AbstractUser:
    # username
    # password
    # first_name
    # last_name
    # email
    # ...
    # Agrega el atributo related_name a los campos de relación
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)
    def __str__(self):
        return self.username
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


class Estacion(models.Model): 
    Id_Lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True) 
    Codigo_Estacion = models.CharField(max_length=20) 
    Nombre = models.CharField(max_length=40)
    Activo = models.BooleanField(default=True)


class Planta(models.Model): 
    Id_Estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True) 
    Codigo_Planta = models.CharField(max_length=20) 
    Nombre = models.CharField(max_length=40) 
    Activo = models.BooleanField(default=True)

    
class Lectura(models.Model): 
    Id_Planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True) 
    E1 = models.IntegerField(default=0, blank=True, null=True)
    E2 = models.IntegerField(default=0, blank=True, null=True)
    E3 = models.IntegerField(default=0, blank=True, null=True)
    E4 = models.IntegerField(default=0, blank=True, null=True)
    E5 = models.IntegerField(default=0, blank=True, null=True)
    Monilla = models.IntegerField(default=0, blank=True, null=True)
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

    
