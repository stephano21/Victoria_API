from rest_framework import serializers
from ..models import Lote
class LoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ('id','Codigo_Lote','Nombre','Hectareas','Variedad','Id_Proyecto', 'Activo')
