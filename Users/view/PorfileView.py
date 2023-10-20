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
class PorfileView(APIView):
    
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            responses={200: "OK"}
        )
    def get(self, request):
        # Extrae los datos del perfil del usuario actual
        try:
            print(request.user.perfil.cedula)
            perfil_data = {
                'cedula': request.user.perfil.cedula,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
            print(perfil_data['username']+" Is logged")
            return Response(perfil_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_204_NO_CONTENT)
         
 