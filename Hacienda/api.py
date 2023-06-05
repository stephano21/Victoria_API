from .models import Hacienda, Proyecto, Lote, Estacion, Planta, Lectura
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import HaciendaSerializers, ProyectoSerializers, LoteSerializers, EstacionSerializers, PlantaSerializers, LecturaSerializers


class HaciendaViewSet(viewsets.ModelViewSet):
    queryset = Hacienda.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = HaciendaSerializers
    def get_queryset(self):
        queryset = super().get_queryset()
        codigo = self.request.query_params.get('id')
        if codigo:
            queryset = queryset.filter(Codigo_Proyecto=codigo)
        return queryset


class ProyectoViewSet(viewsets.ModelViewSet):
    print("aqui")
    queryset = Proyecto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProyectoSerializers
    #filtrar por un id 
    def get_queryset(self):
        queryset = super().get_queryset()
        codigo_proyecto = 2 #self.request.query_params.get('id')
        print(f"luego aqui: {codigo_proyecto}")
        if codigo_proyecto:
            queryset = queryset.filter(Id_Hacienda=codigo_proyecto)
        return queryset

    #filtrar por Id de hacienda
"""  def list(self, request, *args, **kwargs):
    hacienda_id = request.query_params.get('id')
    if hacienda_id:
        queryset = self.queryset.filter(Id_Hacienda_id=hacienda_id)
    else:
        queryset = self.queryset.all()

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data) """

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoteSerializers

    def get_queryset(self):
        queryset = Lote.objects.all()

        id_hacienda = self.kwargs.get('id')  # Obtener el parámetro 'id' de la URL
        if id_hacienda:
            queryset = queryset.filter(Id_Proyecto__Id_Hacienda=id_hacienda)
        return queryset

""" class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoteSerializers
 """

class EstacionViewSet(viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EstacionSerializers

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PlantaSerializers

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LecturaSerializers