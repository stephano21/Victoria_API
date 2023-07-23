from rest_framework import serializers
from .serializer.HaciendaSerializers import HaciendaSerializers
from .serializer.LecturaSerializers import LecturaSerializers
from .serializer.LoteSerializers import LoteSerializers
from .serializer.ProyectoHaciendaSerializer import ProyectoHaciendaSerializer
from .serializer.UserSerializer import UserSerializer
from .serializer.ProyectoSerializers import ProyectoSerializers



""" class PoligonoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Poligono
        fields = ('id','Codigo_Estacion','Nombre','Id_Lote', 'Activo')

class PlantaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ('id','Codigo_Planta','Nombre','Id_Estacion', 'Activo')
 """





