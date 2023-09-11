from rest_framework import serializers
from Clima.models import Daily_Indicadores
class DailyIndicadorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Daily_Indicadores
        fields = ('__all__')
