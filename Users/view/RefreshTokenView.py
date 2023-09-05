from Users.models import Perfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""refresh_token"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class RefreshTokenView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh_token": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["refresh_token"],
        ),
        responses={200: "OK"}
    )
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
            return Response( str(e), status=status.HTTP_400_BAD_REQUEST)