from Hacienda.models import Planta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import PlantaSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class PlantaAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,id,*args, **kwargs):
        user = request.user
        hacienda = request.hacienda_id 
        username = user.username
        print(f"{username} Ha cargado plantas")
        #id = self.kwargs.get('id')
        grupos_usuario = user.groups.all()
        Rol = request.rol
        if hacienda and (Rol != "Researcher" or Rol != "Root"):
            if id: 
                plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Id_Lote = id,
                    Activo=True,
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
                serializer = PlantaSerializers(plantas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if any(grupo.name == "Estudiante" for grupo in grupos_usuario):
                plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Activo=True,
                    VisibleToStudent=True,
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
                serializer = PlantaSerializers(plantas, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if any(grupo.name == "Tecnico" for grupo in grupos_usuario):
                plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Activo=True,
                    VisibleToStudent=True,
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
                serializer = PlantaSerializers(plantas, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif hacienda and (Rol == "Researcher" or Rol == "Root"):
            plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Activo=True,)
            serializer = PlantaSerializers(plantas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)
    

    def post(self, request):
        user = request.user
        username = user.username
        hacienda = request.hacienda_id 
        print(request.data)
        print(f"{username} Ha registrado una planta")
        serializer = PlantaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, id):
        Planta = self.get_object(id)
        serializer = PlantaSerializers(Planta, data=request.data, partial=True)
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
        Planta = self.get_object(id)
        Planta.Activo = False
        Planta.save()

        serializer = PlantaSerializers(Planta)
        return Response(serializer.data)
