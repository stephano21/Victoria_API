from rest_framework import serializers
from ..models import Lectura
class LecturaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ('id','E1','E2','E3','E4','E5','Id_Lote','Monilla', 'Phythptora','Colletotrichum', 'Corynespora', 'Lasodiplodia', 'Cherelles', 'Insectos','Animales','Observacion','FechaVisita', 'Activo')
