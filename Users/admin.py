from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#models
from django.contrib.auth.models import User
from Users.form import CustomUserCreationForm
from Users.models import Perfil
# Register your models here.
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el widget del campo 'user' para mostrar el nombre de la hacienda
        self.fields['user'].widget = forms.Select(choices=[(user.id, user.perfil.nombre_hacienda) for user in User.objects.all()])

""" @admin.register(Perfil)
class UsuarioAdmin(admin.ModelAdmin):
    #form = PerfilForm
    list_display = ("pk", "user", "cedula", "active", "email", 'get_nombre_hacienda')

    def get_nombre_hacienda(self, obj):
        return obj.Id_Hacienda.Nombre if obj.Id_Hacienda else None

    get_nombre_hacienda.short_description = 'Hacienda'

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

    active.short_description = 'Activo' """
class UsuarioInline (admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural= 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email','username', 'password1', 'password2'),
        }),
    )
    list_display = ('username','is_staff', 'get_hacienda_name', 'first_name', 'last_name','get_cedula_number')
    list_display_links = ('is_staff','username','get_cedula_number')
    def get_hacienda_name(self, obj):
        return obj.perfil.Id_Hacienda.Nombre if obj.perfil.Id_Hacienda else None
    
    def get_cedula_number(self, obj):
        return obj.perfil.cedula if obj.perfil.cedula else None

    get_hacienda_name.short_description = 'Hacienda'
    get_cedula_number.short_description = 'Cedula'
   

admin.site.unregister(User)
admin.site.register(User,UserAdmin)