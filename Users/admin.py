from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#models
from django.contrib.auth.models import User
from Users.models import Perfil
# Register your models here.
@admin.register(Perfil)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("pk","user","cedula","active","email",)
    list_display_links = ('pk','cedula','user')
    search_fields = (
        'email', 
        'user',
    )
    list_filter = ('user__is_active','user__is_staff','user__email')
    fieldsets = (
        ('Usuario',{
            'fields':(
                ('cedula','user'),
                ),
        }),
    )
    def email(self, obj):
        return obj.user.email

    email.short_description = 'Correo'
    def active(self, obj):
        return obj.user.is_active

    active.short_description = 'Activo'
class UsuarioInline (admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural= 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)