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
        # Obtén el mes actual (puedes ajustar esto según tus necesidades)
        mes_actual = datetime.now().month

        # Verifica si existe una lectura en ese mes relacionada con la planta
        #return Lectura.objects.filter(Planta__Id_Planta=planta, FechaVisita__month=mes_actual).exists()
        return Lectura.objects.filter(Id_Planta=planta, FechaVisita__month=mes_actual).exists()