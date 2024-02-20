from rest_framework import serializers
from Hacienda.models import Lote,Produccion
import locale
class ProduccionSerializers(serializers.ModelSerializer):
    Lote = serializers.SerializerMethodField()
    Fecha_Produccion = serializers.SerializerMethodField()
    class Meta:
        model = Produccion
        fields = ('__all__')
        required_fields = ('Qq', 'Fecha')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
    def get_Lote(self, instance):
        # Verificar si la instancia de Produccion tiene un Lote asociado
        if instance.Id_Lote:
            return instance.Id_Lote.Codigo_Lote  # Obtener el nombre del lote
        return None  # Manejar el caso en que la relación no existe


    def get_Fecha_Produccion(self, instance):
        if instance.Fecha:
            current_locale = locale.getdefaultlocale()
            try:
                locale.setlocale(locale.LC_TIME, current_locale)
                return instance.Fecha.strftime("%B, %Y")
            except locale.Error:
                return instance.Fecha.strftime("%B, %Y")  # Fallback a un formato estándar si hay un error
        return None

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Qq'] = float(representation['Qq'])
        return representation
