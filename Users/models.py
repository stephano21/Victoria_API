"""Users models"""
from django.contrib.auth.models  import User
from django.db import models
# Create your models here.

class Perfil(models.Model):
    # Campos adicionales, si los necesitas
    # Por ejemplo:
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=10) 
    created = models.DateField(auto_now=True)
    modifief = models.DateField(auto_now=True)

    # Campos heredados de AbstractUser:
    # username
    # password
    # first_name
    # last_name
    # email
    # ...
    
    def __str__(self):
        return self.user.username