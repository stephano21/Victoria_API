from rest_framework import serializers
from Predict.models import DatasetPred
from django.utils import timezone

class DatasetPredSerializer(serializers.ModelSerializer):
    FechaRegistro = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DatasetPred
        fields = '__all__'

    def create(self, validated_data):
        validated_data['FechaRegistro'] = timezone.now()
        return super().create(validated_data)
