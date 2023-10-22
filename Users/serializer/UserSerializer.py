from django.contrib.auth.models import User
from rest_framework import serializers
from Users.models import Perfil
from rest_framework.exceptions import ErrorDetail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Crea un usuario
        perfil_data = self.context.get('perfil_data')  # Obtiene los datos del perfil de contexto
        if perfil_data is None:
            return serializers.ValidationError(["Cedula",[ErrorDetail(string='La cedula es requerida')]])
        
        # Valida que el número de cédula sea único
        cedula = perfil_data.get('cedula')
        if User.objects.filter(perfil__cedula=cedula).exists():
            return serializers.ValidationError(["Cedula",[ErrorDetail(string='El número de cédula ya está en uso')]])
        
        user = User.objects.create_user(**validated_data)
        
        # Crea un perfil asociado a ese usuario
        try:
            Perfil.objects.create(user=user, **perfil_data)
        except Exception as e:
            user.delete()
            return serializers.ValidationError(["Cedula",[ErrorDetail(string='Error al crear el Usuario')]])
        
        return user

