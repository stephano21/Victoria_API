from rest_framework import serializers
from ..models import Usuarios

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['username', 'password', 'email', 'first_name', 'last_name','cedula']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuarios.objects.create_user(**validated_data)
        return user