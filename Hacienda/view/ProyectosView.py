from ..models import Proyecto
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import ProyectoHaciendaSerializer

class ProyectoHaciendaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        hacienda_id = self.kwargs.get('id')
        proyectos = Proyecto.objects.filter(Id_Hacienda_id=hacienda_id).select_related('Id_Hacienda', 'Id_Lote__Id_Estacion__Id_Planta')
        serializer = ProyectoHaciendaSerializer(proyectos, many=True)
        return Response(serializer.data)