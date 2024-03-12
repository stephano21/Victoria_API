from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Hacienda.models import Poligono, GeoCoordenadas, Lote
from Hacienda.serializers import PoligonoSerializers, GeoCoordenadasSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from Users.models import Perfil
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GeoLotesView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        username = user.username
        # Obtener el perfil asociado al usuario
        try:
            id_hacienda = request.hacienda_id
            print(f"{username} Ha cargado Geolotes")
            lote_id = request.query_params.get('lote_id')

            if lote_id:
                poligonos = Poligono.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=id_hacienda,
                    lote__id=lote_id,
                    Activo=True)
            else:
                poligonos = Poligono.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
                    Id_Lote__Id_Proyecto__Id_Hacienda_id=id_hacienda,
                    Activo=True)

            result = []
            for poligono in poligonos:
                poligono_data = PoligonoSerializers(poligono).data
                geocoordenadas = GeoCoordenadas.objects.filter(
                    Id_Poligono=poligono.id, Activo=True)
                geocoordenadas_data = GeoCoordenadasSerializers(
                    geocoordenadas, many=True).data
                # Obtener el nombre del lote correspondiente usando la relación ForeignKey
                nombre_lote = poligono.Id_Lote.Nombre if poligono.Id_Lote else None
                codigo_lote = poligono.Id_Lote.Codigo_Lote if poligono.Id_Lote else None
                poligono_data['Lote'] = nombre_lote
                poligono_data['CodigoLote'] = codigo_lote
                poligono_data['geocoordenadas'] = geocoordenadas_data
                result.append(poligono_data)
            print(result)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            # Manejar el caso en el que el perfil no existe para el usuario
            return Response(f"Ocurrio un erro: {str(e)}", status=status.HTTP_400_BAD_REQUEST_)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "poligono": openapi.Schema(type=openapi.TYPE_OBJECT),
                "geocoordenadas": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            },
            required=["poligono"],
            example={

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
        ),
        responses={201: "Created"}
    )
    def post(self, request):
        # Verificar si ya existe un polígono registrado para el lote
        lote_id = request.data.get('Id_Lote')
        user = request.user
        username = user.username
        print(f"{username} Ha registrado un Geolote")
        if Poligono.objects.filter(Id_Lote=lote_id, Activo=True).exists():
            return Response("Ya existe un polígono registrado para este lote.", status=status.HTTP_400_BAD_REQUEST)

        poligono_serializer = PoligonoSerializers(
            data=request.data)
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
            serializer.validated_data['Id_Poligono'] = poligono
            serializer.save()

            # Enviar la respuesta
        return Response(request.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[  # Define el parámetro manualmente
            openapi.Parameter(
                'id', openapi.IN_PATH, description="ID del polígono a eliminar", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: "El polígono y sus geocoordenadas han sido eliminados con éxito.",
            404: "El polígono no existe.",
        }
    )
    def delete(self, request, id):
        """
        Elimina un polígono y sus geocoordenadas.

        Esta vista elimina un polígono identificado por su ID y también marca como
        inactivas todas las geocoordenadas asociadas a ese polígono.

        Args:
            request (HttpRequest): La solicitud HTTP DELETE.
            id (int): El ID del polígono a eliminar.

        Returns:
            Response: Un objeto de respuesta con un mensaje de éxito o error.
        """
        try:
            user = request.user
            username = user.username
            print(f"{username} Ha eliminado un Geolote")
            poligono = get_object_or_404(Poligono, pk=id, Activo=True)
            print(poligono)
            if not poligono:
                return Response("El polígono no existe.", status=status.HTTP_404_NOT_FOUND)
        except Poligono.DoesNotExist:
            return Response("El polígono no existe.", status=status.HTTP_404_NOT_FOUND)

        # Actualizar el campo "activo" del polígono y sus geocoordenadas
        poligono.Activo = False
        print(Poligono)
        poligono.save()

        geocoordenadas = GeoCoordenadas.objects.filter(Id_Poligono=poligono)
        for geocoordenada in geocoordenadas:
            geocoordenada.Activo = False
            geocoordenada.save()

        return Response("El polígono y sus geocoordenadas han sido eliminados con éxito.", status=status.HTTP_200_OK)
