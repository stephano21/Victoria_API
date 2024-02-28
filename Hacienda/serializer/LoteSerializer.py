from rest_framework import serializers
from Hacienda.models import Lote, Poligono
from Hacienda.serializer.PoligonoSerializer import PoligonoSerializers
class LoteSerializers(serializers.ModelSerializer):
    poligonos = PoligonoSerializers(many=True, write_only=True, required=False)
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
