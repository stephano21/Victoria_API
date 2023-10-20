from Users.models import Perfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=["username", "password"],
            example={
                "username": "your_username",
                "password": "your_password"
            }
        ),
        responses={200: "OK"}
    )
    def post(self, request):
        # Obtiene los datos de inicio de sesión del cuerpo de la solicitud
        username = request.data.get('username')
        password = request.data.get('password')

        # Obtiene el modelo de usuario personalizado (Perfil en tu caso)
        User = get_user_model()

        try:
            # Intenta obtener el usuario basado en el nombre de usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('Usuario no registrado', status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            # Genera los tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            print(f"{username} Ha iniciado sesión")

            # Retorna los tokens en la respuesta
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            })
        else:
            print(username+" Credenciales incorrectas ")
            return Response('Credenciales inválidas', status=status.HTTP_401_UNAUTHORIZED)
 