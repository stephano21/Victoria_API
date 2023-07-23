from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Poligono, GeoCoordenadas
from ..serializers import PoligonoSerializers, GeoCoordenadasSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from ..interfaces.ResponseApi import ResponseApi
class GeoLotesView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lote_id = request.query_params.get('lote_id')  # Obtener el ID del lote desde los parámetros de la URL

        if lote_id:
            poligonos = Poligono.objects.filter(Id_Lote=lote_id)
            geocoordenadas = GeoCoordenadas.objects.filter(Id_Poligono__Id_Lote=lote_id)
        else:
            poligonos = Poligono.objects.all()
            geocoordenadas = GeoCoordenadas.objects.all()

        poligono_serializer = PoligonoSerializers(poligonos, many=True)
        geocoordenadas_serializer = GeoCoordenadasSerializers(geocoordenadas, many=True)

        return Response({
            "poligonos": poligono_serializer.data,
            "geocoordenadas": geocoordenadas_serializer.data
        }, status=status.HTTP_200_OK)
    

    def post(self, request):
        poligono_serializer = PoligonoSerializers(data=request.data.get('poligono', {}))
        if not poligono_serializer.is_valid():
            return Response(poligono_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        geocoordenadas_data = request.data.get('geocoordenadas', [])
        geocoordenadas_serializers = [GeoCoordenadasSerializers(data=data) for data in geocoordenadas_data]

        for serializer in geocoordenadas_serializers:
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        poligono = poligono_serializer.save()

        for serializer in geocoordenadas_serializers:
            serializer.save(Id_Poligono=poligono)


        message = "Operación exitosa."
        detail = "Poligono y Geocoordenadas creados correctamente."
        success = True

        # Crear el objeto ResponseApi
        response_data = ResponseApi(message=message, detail=detail, success=success)

        # Enviar la respuesta
        return Response(response_data.__dict__, status=status.HTTP_201_CREATED)