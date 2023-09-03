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
                "username": "your_username",
                "password": "your_password"
            }
        ),
        responses={200: "OK"}   
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Usuario registrado correctamente")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)