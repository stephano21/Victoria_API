from django.shortcuts import render
from .models import Proyecto, Lote
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
from .serializers import ProyectoHaciendaSerializer, LoteSerializers
# Create your views here.
class ProyectoHaciendaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        hacienda_id = self.kwargs.get('id')
        proyectos = Proyecto.objects.filter(Id_Hacienda_id=hacienda_id).select_related('Id_Hacienda', 'Id_Lote__Id_Estacion__Id_Planta')
        serializer = ProyectoHaciendaSerializer(proyectos, many=True)
        return Response(serializer.data)

class LoteAPIView(APIView):
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
        serializer = LoteSerializers(lote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    