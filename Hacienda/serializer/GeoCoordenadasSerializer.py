from rest_framework import serializers
from ..models import GeoCoordenadas

class GeoCoordenadasSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeoCoordenadas
        fields = ('id','Id_Poligono','lat','lng','Activo')