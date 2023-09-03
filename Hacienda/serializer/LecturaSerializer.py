from rest_framework import serializers
from ..models import Lectura
class LecturaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ('__all__')
