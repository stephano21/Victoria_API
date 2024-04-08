from rest_framework import serializers
from Predict.models import DatasetTrain
from django.utils import timezone

class DatasetTrainSerializer(serializers.ModelSerializer):
    FechaRegistro = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DatasetTrain
        fields = '__all__'

    def create(self, validated_data):
        validated_data['FechaRegistro'] = timezone.now()
        return super().create(validated_data)
