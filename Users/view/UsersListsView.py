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

from Users.serializer.UserSerializer import UserSerializer

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UsuarioList(APIView):
    """ def get(self, request, format=None):
        usuarios = Perfil.objects.all()
        serializer = UserSerializer.PerfilSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) """

    def get(self, request, format=None):
        usuarios = User.objects.all()
        print(usuarios)
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)