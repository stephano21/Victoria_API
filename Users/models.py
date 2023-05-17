from django.db import models

# Create your models here.


class Users (models.Model):
    Name = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Username = models.CharField(max_length=10)
    Password = models.CharField(max_length=100,null=False)
    Activo = models.BooleanField()