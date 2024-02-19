from rest_framework import serializers
from Predict.models import Dataset
from django.utils import timezone

class DatasetSerializer(serializers.ModelSerializer):
    FechaRegistro = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        validated_data['FechaRegistro'] = timezone.now()
        return super().create(validated_data)
