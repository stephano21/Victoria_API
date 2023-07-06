from rest_framework import serializers
from .models import Hacienda, Proyecto, Lote, Estacion, Planta, Lectura

class HaciendaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hacienda
        fields = ('id','codigo','Nombre', 'Activo')

class ProyectoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('id','Codigo_Proyecto','Nombre','Id_Hacienda', 'Activo')

class LoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ('id','Codigo_Lote','Nombre','Hectareas','Variedad','Id_Proyecto', 'Activo')

class EstacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estacion
        fields = ('id','Codigo_Estacion','Nombre','Id_Lote', 'Activo')

class PlantaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ('id','Codigo_Planta','Nombre','Id_Estacion', 'Activo')

class LecturaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ('id','E1','E2','E3','E4','E5','Id_Planta','Monilla', 'Phythptora','Colletotrichum', 'Corynespora', 'Lasodiplodia', 'Cherelles', 'Insectos','Animales','Observacion', 'Id_Planta', 'Activo')


class ProyectoHaciendaSerializer(serializers.ModelSerializer):
    # Define los campos que deseas mostrar en el resultado
    class Meta:
        model = Proyecto
        fields = '__all__'


