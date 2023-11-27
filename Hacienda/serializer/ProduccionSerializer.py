from rest_framework import serializers
from Hacienda.models import Lote,Produccion

class ProduccionSerializers(serializers.ModelSerializer):
    Disabled = serializers.SerializerMethodField()
    class Meta:
        model = Produccion
        fields = ('__all__')
        required_fields = ('Qq', 'Fecha')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
    