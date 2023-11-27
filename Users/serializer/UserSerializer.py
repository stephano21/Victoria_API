from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from Hacienda.models import Hacienda
from Users.models import Perfil
from rest_framework.exceptions import ErrorDetail
class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    def validar_cedula(self, cedula):
        # Verificar longitud de la cédula
        if len(cedula) != 10:
            raise ValidationError(["Cedula",[ErrorDetail(string="La longitud debe ser de 10 dígitos.")]])
        
        # Verificar que todos los caracteres sean dígitos
        if not cedula.isdigit():
            raise ValidationError(["Cedula",[ErrorDetail(string="Debe contener solo dígitos.")]])
        
        provincia = int(cedula[:2])
        if (provincia < 1 or provincia > 24) and provincia != 30:
            raise ValidationError(["Cedula",[ErrorDetail(string="La provincia no es válida.")]])
        # Obtener los primeros 9 dígitos
        digitos = list(map(int, cedula[:-1]))

        # Aplicar el algoritmo de Luhn
        for i in range(0, 9, 2):
            digitos[i] *= 2
            if digitos[i] > 9:
                digitos[i] -= 9

        suma_total = sum(digitos)
        digito_verificador = (10 - (suma_total % 10)) % 10

        # Comparar el dígito verificador calculado con el dígito verificador proporcionado
        return digito_verificador == int(cedula[-1])
    
    perfil = PerfilSerializer(required=False)
    class Meta:
        model = User
        fields = '__all__'#['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Crea un usuario
        perfil_data = self.context.get('perfil_data')  # Obtiene los datos del perfil de contexto
        if perfil_data is None:
            return serializers.ValidationError(["Cedula",[ErrorDetail(string='La cedula es requerida')]])
        
        Id_Hacienda = perfil_data.get('Id_Hacienda')
        # Valida que el número de cédula sea único
        cedula = perfil_data.get('cedula')
        if not self.validar_cedula(cedula):
            print("El número de cédula es inválido!")
            raise ValidationError(["Cedula",[ErrorDetail(string='El número de cédula es inválido!')]])
        
        if User.objects.filter(perfil__cedula=cedula).exists():
            raise ValidationError(["Cedula",[ErrorDetail(string='El número de cédula ya está en uso!')]])
        print("Creando usuario...")
        user = User.objects.create_user(**validated_data)
        print("Usuario creado:", user.username)
        # Intenta convertir el valor de cadena a una instancia de Hacienda
        Id_Hacienda_value = perfil_data.get('Id_Hacienda')
        hacienda_instance = get_object_or_404(Hacienda, id=Id_Hacienda_value)
        # Quita 'Id_Hacienda' de perfil_data antes de crear la instancia de Perfil
        perfil_data.pop('Id_Hacienda', None)
        # Crea un perfil asociado a ese usuario
        try:
            print("Creando perfil...")
            perfil = Perfil.objects.create(user=user, Id_Hacienda=hacienda_instance, **perfil_data)
            print("Perfil creado:", Perfil.cedula)
        except Exception as e:
            user.delete()
            print("Error al crear el perfil:", e)
            return serializers.ValidationError(["Cedula",[ErrorDetail(string='Error al crear el Usuario')]])
        
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        perfil_data = representation.pop('perfil', None)
        if perfil_data is not None:
            for key, value in perfil_data.items():
                representation[key] = value
        return representation

