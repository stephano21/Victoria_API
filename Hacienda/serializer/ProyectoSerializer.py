from rest_framework import serializers
from ..models import Proyecto
class ProyectoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('__all__')
