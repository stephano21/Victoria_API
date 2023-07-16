from django.shortcuts import render
from .models import Proyecto, Lote,Estacion,Planta,Usuarios
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProyectoHaciendaSerializer, LoteSerializers,EstacionSerializers, PlantaSerializers,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated




# Create your views here.
class ProyectoHaciendaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        hacienda_id = self.kwargs.get('id')
        proyectos = Proyecto.objects.filter(Id_Hacienda_id=hacienda_id).select_related('Id_Hacienda', 'Id_Lote__Id_Estacion__Id_Planta')
        serializer = ProyectoHaciendaSerializer(proyectos, many=True)
        return Response(serializer.data)
#lotes

class LoteAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        id = self.kwargs.get('id')
        if id: 
            lotes = Lote.objects.filter(Id_Proyecto = id)
            serializer = LoteSerializers(lotes, many=True)
            return Response(serializer.data)

        lotes = Lote.objects.all()
        serializer = LoteSerializers(lotes, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = LoteSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        lote = self.get_object(pk)
        serializer = LoteSerializers(lote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Lote.objects.get(pk=pk)
        except Lote.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request, id):
        lote = self.get_object(id)
        lote.Activo = False
        lote.save()

        serializer = LoteSerializers(lote)
        return Response(serializer.data)

#estaciones
class EstacionAPIView(APIView):
    # Código existente...
    def get(self, request,*args, **kwargs):
        id = self.kwargs.get('id')
        if id: 
            estaciones = Estacion.objects.filter(Id_Lote = id)
            serializer = EstacionSerializers(estaciones, many=True)
            return Response(serializer.data)

        estaciones = Estacion.objects.all()
        serializer = EstacionSerializers(estaciones, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = EstacionSerializers(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['Nombre']
            if Estacion.objects.filter(nombre=nombre).exists():
                return Response({'error': f'El nombre: {nombre} ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        estacion = self.get_object(pk)
        serializer = EstacionSerializers(estacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Estacion.objects.get(pk=pk)
        except Estacion.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request, id):
        estacion = self.get_object(id)
        estacion.Activo = False
        estacion.save()

        serializer = EstacionSerializers(estacion)
        return Response(serializer.data)

#plantas
class PlantaAPIView(APIView):
    # Código existente...
    def get(self, request,*args, **kwargs):
        id = self.kwargs.get('id')
        if id: 
            plantas = Planta.objects.filter(Id_Estacion = id)
            serializer = PlantaSerializers(plantas, many=True)
            return Response(serializer.data)

        plantas = Planta.objects.all()
        serializer = PlantaSerializers(plantas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlantaSerializers(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['Nombre']
            if Planta.objects.filter(nombre=nombre).exists():
                return Response({'error': f'El nombre: {nombre} ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request, pk):
        planta = self.get_object(pk)
        serializer = PlantaSerializers(planta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Planta.objects.get(pk=pk)
        except Planta.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request, id):
        planta = self.get_object(id)
        planta.Activo = False
        planta.save()

        serializer = PlantaSerializers(planta)
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Realiza la autenticación del usuario
        user = Usuarios.objects.get(username=username)
        if user.check_password(password):
            # Genera los tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Retorna los tokens en la respuesta
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)