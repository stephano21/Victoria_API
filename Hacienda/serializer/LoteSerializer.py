from rest_framework import serializers
from ..models import Lote
from .PoligonoSerializer import PoligonoSerializers
class LoteSerializers(serializers.ModelSerializer):
    poligonos = PoligonoSerializers(many=True, read_only=True)
    class Meta:
        model = Lote
        fields = '__all__'
