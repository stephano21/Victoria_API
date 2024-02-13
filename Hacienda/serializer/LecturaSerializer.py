from rest_framework import serializers
from Hacienda.models import Lectura
class LecturaSerializers(serializers.ModelSerializer):
    NombrePlanta = serializers.SerializerMethodField()
    class Meta:
        model = Lectura
        fields = ('__all__')
        required_fields = ('SyncId', 'FechaVisita')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
    def get_NombrePlanta(self, instance):
        # Verificar si la instancia de Produccion tiene un Lote asociado
        if instance.Id_Planta:
            # Verificar si el Lote tiene un Proyecto asociado
            return instance.Id_Planta.Nombre
        return None  # Manejar el caso en que la relación no existe
