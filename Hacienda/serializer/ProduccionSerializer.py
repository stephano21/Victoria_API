from rest_framework import serializers
from Hacienda.models import Lote,Produccion
import locale
class ProduccionSerializers(serializers.ModelSerializer):
    Victoria = serializers.SerializerMethodField()
    #Fecha = serializers.SerializerMethodField()
    class Meta:
        model = Produccion
        fields = ('__all__')
        required_fields = ('Qq', 'Fecha')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
    def get_Victoria(self, instance):
        # Verificar si la instancia de Produccion tiene un Lote asociado
        if instance.Id_Lote:
            # Verificar si el Lote tiene un Proyecto asociado
            if instance.Id_Lote.Id_Proyecto:
                # Devolver el Nombre del Proyecto
                return instance.Id_Lote.Id_Proyecto.Nombre
        return None  # Manejar el caso en que la relación no existe


    def get_Fecha_Produccion(self, instance):
        # Aquí puedes formatear la fecha según tus requisitos
        # Configura la localización a español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')  # Ajusta la localización según tu sistema

        if instance.Fecha:
            return instance.Fecha.strftime("%B, %Y")
        return None  # Puedes manejar el caso en que la fecha sea nula según tus necesidades
