from Users.models import Perfil
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from Users.serializer.AsignacionGrupoSerializer import AsignacionGrupoSerializer

from Users.serializer.GroupSerializer import GroupSerializer

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GrupoList(APIView):
    def get(self, request, format=None):
        grupos = Group.objects.all()
        serializer = GroupSerializer(grupos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = AsignacionGrupoSerializer(data=request.data)
        if serializer.is_valid():
            usuario_id = request.data.get('usuario_id')
            grupo_id = request.data.get('grupo_id')
            try:
                usuario = User.objects.get(id=usuario_id)
                grupo = Group.objects.get(id=grupo_id)
                usuario.groups.add(grupo)
                usuario.save()
                return Response({"mensaje": "Grupo asignado con éxito"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Group.DoesNotExist:
                return Response({"mensaje": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
