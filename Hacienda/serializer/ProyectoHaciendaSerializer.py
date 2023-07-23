from rest_framework import serializers
from ..models import Proyecto
class ProyectoHaciendaSerializer(serializers.ModelSerializer):
    # Define los campos que deseas mostrar en el resultado
    class Meta:
        model = Proyecto
        fields = '__all__'