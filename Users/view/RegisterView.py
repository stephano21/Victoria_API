from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Users.serializer.UserSerializer import UserSerializer
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    @swagger_auto_schema(
       request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=["username", "password"],
            example={
                "cedula":"number",
                "username": "string",
                "email":"email",
                "first_name":"string",
                "last_name":"string",
                "password":"string",
            }
        ),
        responses={200: "OK"}   
    )
    def post(self, request):
         # Extrae los datos del perfil de la solicitud
        perfil_data = {
            'cedula': request.data.get('cedula', ''),
        }
        
        # Crea un serializer de usuario pasando los datos del perfil en el contexto
        serializer_data = {
            'username': request.data.get('username', ''),
            'password': request.data.get('password', ''),
            'email': request.data.get('email', ''),
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
        }
        
        serializer = UserSerializer(data=serializer_data, context={'perfil_data': perfil_data})
        
        if serializer.is_valid():
            serializer.save()
            return Response("Usuario registrado correctamente")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)