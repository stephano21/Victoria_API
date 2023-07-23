from rest_framework import serializers
from ..models import Poligono
class PoligonoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Poligono
        fields = ('id','FillColor','Id_Lote', 'Activo')