from Hacienda.models import Proyecto
from rest_framework.views import APIView
from rest_framework.response import Response
from Hacienda.serializers import ProyectoSerializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
class ProyectoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        id_hacienda = request.hacienda_id 
        id = self.kwargs.get('id')
        proyectos = Proyecto.objects.select_related('Id_Hacienda').filter(
            Activo=True,
            Id_Hacienda_id=id_hacienda,
            )
        serializer = ProyectoSerializers(proyectos, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_NUMBER),
                "Codigo_Proyecto": openapi.Schema(type=openapi.TYPE_STRING),
                "Nombre": openapi.Schema(type=openapi.TYPE_STRING),
                "Densidad": openapi.Schema(type=openapi.TYPE_STRING),
                "Activo": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "Usuario": openapi.Schema(type=openapi.TYPE_STRING),
                "Id_Hacienda": openapi.Schema(type=openapi.TYPE_NUMBER)
            },
            required=["username", "password"],
            example={
                "id": 1,
                "Codigo_Proyecto": "HV_V1",
                "Nombre": "Victoria 1",
                "Densidad": "null",
                "Activo": "true",
                "Usuario": "rzambrano",
                "Id_Hacienda": 1
            }
        ),
        responses={200: "OK"}
    )
    def post(self, request):
        id_hacienda = request.hacienda_id 
        if not id_hacienda:  return Response( "No se ha encontrado el id de la hacienda", status=status.HTTP_400_BAD_REQUEST)
        request.data["Id_Hacienda"]=id_hacienda
        print(request.data)
        serializer = ProyectoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
