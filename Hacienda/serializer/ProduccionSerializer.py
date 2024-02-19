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
        # Aquí puedes formatear la fecha según tus requisitos
        # Configura la localización a español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')  # Ajusta la localización según tu sistema

        if instance.Fecha:
            return instance.Fecha.strftime("%B, %Y")
        return None  # Puedes manejar el caso en que la fecha sea nula según tus necesidades
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Qq'] = float(representation['Qq'])
        return representation
