from rest_framework import serializers
from Hacienda.models import Planta
class PlantaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ('__all__')
        required_fields = ('Codigo_Planta', 'Nombre')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
