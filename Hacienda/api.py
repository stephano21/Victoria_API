from .models import Hacienda, Proyecto, Lote, Lectura
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import HaciendaSerializers, ProyectoSerializers, LoteSerializers, LecturaSerializers


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


""" class EstacionViewSet(viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EstacionSerializers """
""" 
class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PlantaSerializers """

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LecturaSerializers