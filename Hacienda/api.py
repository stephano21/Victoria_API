from .models import Hacienda, Proyecto, Lectura
from rest_framework import viewsets, permissions
from .serializers import HaciendaSerializers, ProyectoSerializers, LecturaSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class HaciendaViewSet(viewsets.ModelViewSet):
    queryset = Hacienda.objects.filter(Activo=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = HaciendaSerializers
    def get_queryset(self):
        queryset = super().get_queryset()
        codigo = self.request.query_params.get('cod')
        if codigo:
            queryset = queryset.filter(codigo=codigo)
        return queryset


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.filter(Activo=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = ProyectoSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        codigo_proyecto = self.request.query_params.get('cod')
        if codigo_proyecto:
            queryset = queryset.filter(Codigo_Proyecto=codigo_proyecto)
        return queryset

