from Users.models import Perfil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

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

        try:
            # Intenta obtener el usuario basado en el nombre de usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print('Usuario no registrado')
            return Response('Usuario no registrado', status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            # Obtiene el primer grupo al que pertenece el usuario (si hay alguno)
            user_groups = user.groups.all()
            print(user_groups)
            first_group_name = user_groups.last().name if user_groups else None

            # Obtiene los permisos del usuario
            user_permissions = user.user_permissions.all()
            # Convierte los permisos en una lista de nombres
            permission_names = [permission.codename for permission in user_permissions]

            # Genera los tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            print(f"{username} Ha iniciado sesión")

            # Retorna los tokens y la lista de nombres de permisos en la respuesta
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'permissions': permission_names,
                'rol': first_group_name,
                'usurio': username,
                'hacienda': user.perfil.Id_Hacienda.Nombre if not user.perfil.Id_Hacienda == None else"",
            })
        else:
            print(username + " Credenciales incorrectas ")
            return Response('Credenciales inválidas', status=status.HTTP_401_UNAUTHORIZED)
