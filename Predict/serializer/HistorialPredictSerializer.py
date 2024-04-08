from rest_framework import serializers
from Predict.models import HistorialPredict
from django.utils import timezone


class HistorialPredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPredict
        fields = '__all__'

    def create(self, validated_data):
        validated_data['FechaRegistro'] = timezone.now()
        return super().create(validated_data)
