from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Poligono, GeoCoordenadas, Lote
from ..serializers import PoligonoSerializers, GeoCoordenadasSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from ..interfaces.ResponseApi import ResponseApi
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GeoLotesView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    """ @swagger_auto_schema(
        method='get',
        operation_description="Custom description for GET request",
        responses={200: "Successful response"}
    ) """

    def get(self, request):
        lote_id = request.query_params.get('lote_id')

        if lote_id:
            poligonos = Poligono.objects.filter(lote__id=lote_id)
        else:
            poligonos = Poligono.objects.all()

        result = []
        for poligono in poligonos:
            poligono_data = PoligonoSerializers(poligono).data
            geocoordenadas = GeoCoordenadas.objects.filter(
                Id_Poligono=poligono.id)
            geocoordenadas_data = GeoCoordenadasSerializers(
                geocoordenadas, many=True).data
            # Obtener el nombre del lote correspondiente usando la relación ForeignKey
            nombre_lote = poligono.Id_Lote.Nombre if poligono.Id_Lote else None
            poligono_data['Lote'] = nombre_lote
            poligono_data['geocoordenadas'] = geocoordenadas_data
            result.append(poligono_data)

        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "poligono": openapi.Schema(type=openapi.TYPE_OBJECT),
                "geocoordenadas": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            },
            required=["poligono"],
            example={
                "poligono": {
                    "id": 1,
                    "FillColor": "#FF0000",
                    "Activo": True,
                    "Id_Lote": 1,
                    "geocoordenadas": [
                        {
                            "id": 1,
                            "Id_Poligono": 1,
                            "lat": "40.7128000000000000",
                            "lng": "-74.0060000000000000",
                            "Activo": True
                        }
                    ]
                }

            }
        ),
        responses={201: "Created"}
    )
    def post(self, request):
        # Verificar si ya existe un polígono registrado para el lote
        lote_id = request.data.get('poligono', {}).get('Id_Lote')
        
        if Poligono.objects.filter(Id_Lote=lote_id).exists():
            message = "Operación fallida."
            detail = "Ya existe un polígono registrado para este lote."
            success = False
            # Crear el objeto ResponseApi
            response_data = ResponseApi(
            message=message, detail=detail, success=success)
            return Response(response_data.__dict__, status=status.HTTP_400_BAD_REQUEST)
            #return Response({"message": "Ya existe un polígono registrado para este lote."}, status=status.HTTP_400_BAD_REQUEST)

        poligono_serializer = PoligonoSerializers(
            data=request.data.get('poligono', {}))
        if not poligono_serializer.is_valid():
            return Response(poligono_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        geocoordenadas_data = request.data.get('geocoordenadas', [])
        geocoordenadas_serializers = [GeoCoordenadasSerializers(
            data=data) for data in geocoordenadas_data]

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
        response_data = ResponseApi(
            message=message, detail=detail, success=success)

        # Enviar la respuesta
        return Response(request.data, status=status.HTTP_201_CREATED)
