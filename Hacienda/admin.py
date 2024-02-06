from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#models
from django.contrib.auth.models import User
from Users.form import CustomUserCreationForm
from Hacienda.models import Hacienda
# Register your models here.

class HaciendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'activo', 'usuario')  # Campos que se mostrarán en la lista de objetos

    def nombre(self, obj):
        return obj.Nombre

    def codigo(self, obj):
        return obj.codigo

    def activo(self, obj):
        return obj.Activo

    def usuario(self, obj):
        return obj.Usuario
admin.site.register(Hacienda, HaciendaAdmin)
admin.site.unregister(User)
admin.site.register(User,HaciendaAdmin)
