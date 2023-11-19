from Users.models import Perfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

from Users.serializer.GroupSerializer import GroupSerializer

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GrupoList(APIView):
    def get(self, request, format=None):
        grupos = Group.objects.all()
        serializer = GroupSerializer(grupos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)