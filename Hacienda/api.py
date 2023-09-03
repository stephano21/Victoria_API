from .models import Hacienda, Proyecto, Lectura
from rest_framework import viewsets, permissions
from .serializers import HaciendaSerializers, ProyectoSerializers, LecturaSerializers


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

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LecturaSerializers