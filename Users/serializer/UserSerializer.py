from rest_framework import serializers
from Users.models import Perfil

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['username', 'password', 'email', 'first_name', 'last_name','cedula']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Perfil.objects.create_user(**validated_data)
        return user