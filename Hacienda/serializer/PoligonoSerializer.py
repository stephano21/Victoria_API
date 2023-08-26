from rest_framework import serializers
from ..models import Poligono
from .GeoCoordenadasSerializer import GeoCoordenadasSerializers
class PoligonoSerializers(serializers.ModelSerializer):
    coordenadas = GeoCoordenadasSerializers(many=True, read_only=True) 
    class Meta:
        model = Poligono
        fields = '__all__'