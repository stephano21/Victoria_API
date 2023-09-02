from Users.models import Perfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class RefreshTokenView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtén el refresh_token del cuerpo de la solicitud.
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"error": "El refresh_token es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta refrescar el token.
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({"access_token": access_token, "message": "Token de acceso actualizado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "No se pudo actualizar el token de acceso"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        # Obtén el refresh_token del cuerpo de la solicitud.
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response("El refresh_token es requerido", status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta refrescar el token.
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            return Response({"access_token": access_token, "refresh_token": new_refresh_token}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response( "No se pudo actualizar los tokens", status=status.HTTP_400_BAD_REQUEST)