from Hacienda.models import Planta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import PlantaSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.ValidatorHelper import GetIdPlanta


class PlantaAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...

    def get(self, request, *args, **kwargs):
        user = request.user
        hacienda = request.hacienda_id
        username = user.username
        print(f"{username} Ha cargado plantas")
        id = self.kwargs.get('id')
        grupos_usuario = user.groups.all()
        Rol = request.rol
        if hacienda:
            print(f"have hacienda{hacienda}")
            # Filtrar plantas basado en diferentes condiciones según el rol
            if Rol not in ["Researcher", "Root"]:
                plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Activo=True,
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda
                )
            else:
                plantas = Planta.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Activo=True,
                )

            if any(grupo.name == "Estudiante" for grupo in grupos_usuario):
                plantas = plantas.filter(VisibleToStudent=True)

            elif any(grupo.name == "Tecnico" for grupo in grupos_usuario):
                print(f"es tecnico")
                plantas = plantas.filter(VisibleToStudent=True)

            serializer = PlantaSerializers(plantas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        username = user.username
        hacienda = request.hacienda_id
        ExistePlanta = GetIdPlanta(request.data['Codigo_Planta'], hacienda)
        if ExistePlanta:
            return Response(f"La planta {request.data['Codigo_Planta']} ya existe!", status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        print(f"{username} Ha registrado una planta")
        serializer = PlantaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        Planta = self.get_object(id)
        serializer = PlantaSerializers(Planta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(f"Planta {Planta.Codigo_Planta} actualizada con éxito", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Planta.objects.get(pk=pk)
        except Planta.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete(self, request, id):
        Planta = self.get_object(id)
        Planta.Activo = False
        Planta.save()
        return Response(f"Se ha eliminado la planta {Planta.Codigo_Planta} ", status=status.HTTP_200_OK)
