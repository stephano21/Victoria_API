from rest_framework import serializers
from Hacienda.models import Lectura
class LecturaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ('__all__')
        required_fields = ('SyncId', 'FechaVisita')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
