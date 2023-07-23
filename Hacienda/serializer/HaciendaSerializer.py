from rest_framework import serializers
from ..models import Hacienda

class HaciendaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hacienda
        fields = ('id','codigo','Nombre', 'Activo')
