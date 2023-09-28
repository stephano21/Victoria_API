from rest_framework import serializers
from Hacienda.models import Planta,Lectura
from datetime import datetime, timedelta
class PlantaSerializers(serializers.ModelSerializer):
    Disabled = serializers.SerializerMethodField()
    class Meta:
        model = Planta
        fields = ('__all__')
        required_fields = ('Codigo_Planta', 'Nombre')
        extra_kwargs = {
            field: {'required': True}
            for field in required_fields
        }
    def get_Disabled(self, planta):
        # Obtén el mes y año actual
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.month
        año_actual = fecha_actual.year

        # Verifica si existe una lectura en ese mes y año relacionada con la planta
        return Lectura.objects.filter(Id_Planta=planta, FechaVisita__month=mes_actual, FechaVisita__year=año_actual).exists()
