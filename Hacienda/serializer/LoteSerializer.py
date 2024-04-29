from rest_framework import serializers
from Hacienda.models import Lote, Poligono
from Hacienda.serializer.PoligonoSerializer import PoligonoSerializers
from datetime import datetime
class LoteSerializers(serializers.ModelSerializer):
    poligonos = PoligonoSerializers(many=True, write_only=True, required=False)
    edad_real= serializers.SerializerMethodField()
    class Meta:
        model = Lote
        fields = '__all__'

    def create(self, validated_data):
        poligonos_data = validated_data.pop('poligonos', None)

        lote = Lote.objects.create(**validated_data)
        if poligonos_data:
            for poligono_data in poligonos_data:
                print(poligono_data)
                Poligono.objects.create(Id_Lote=lote, **poligono_data)
        return lote
    def get_edad_real(self, instance):
        if instance.FechaSiembra is None:
            return None
        fecha_siembra = instance.FechaSiembra
        fecha_actual = datetime.now().date()
        edad_real = fecha_actual.year - fecha_siembra.year
        if fecha_actual.month < fecha_siembra.month or (fecha_actual.month == fecha_siembra.month and fecha_actual.day < fecha_siembra.day):
            edad_real -= 1
        return edad_real
