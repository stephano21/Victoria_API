from rest_framework import serializers
from django.contrib.auth.models import User, Group

class AsignacionGrupoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    grupo_id = serializers.IntegerField()