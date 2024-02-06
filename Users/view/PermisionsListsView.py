from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.serializer.PemisionsSerializer import PermisionsSerializer
from django.contrib.auth.models import Permission
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PermisionsList(APIView):
    """vjsdbfvjbf"""
   
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # Lógica para obtener todos los permisos de DRF
        permisos = self.get_drf_permissions()
        
        # Lógica para serializar los permisos
        permisos_serializer = PermisionsSerializer(permisos, many=True)
        
        # Devolver la respuesta
        return Response(permisos_serializer.data, status=status.HTTP_200_OK)

    def get_drf_permissions(self):
        # Obtener todos los permisos de DRF
        drf_permissions = Permission.objects.all()
        return drf_permissions

