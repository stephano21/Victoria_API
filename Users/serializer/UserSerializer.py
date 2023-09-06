from django.contrib.auth.models import User
from rest_framework import serializers
from Users.models import Perfil

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Cambia el modelo a User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Crea un usuario
        user = User.objects.create_user(**validated_data)
        
        # Crea un perfil asociado a ese usuario
        perfil_data = self.context.get('perfil_data')  # Obtiene los datos del perfil de contexto
        Perfil.objects.create(user=user, **perfil_data)
        
        return user