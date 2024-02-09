from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""Security"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""Models and Serializers"""
from Hacienda.models import Planta
from Hacienda.serializers import PlantaSerializers
import pandas as pd
from datetime import datetime
import uuid
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Hacienda.validators.ValidatorHelper import Validate_Headers_Excel,GetIdPlanta, GetIdLote
class ImportPlantasView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_FILE,
            
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Datos cargados correctamente',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'mensaje': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Mensaje de éxito'
                        )
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Error al cargar los datos',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Mensaje de error'
                        )
                    }
                )
            )
        }
        
    )
    def post(self, request):
        archivo_excel = request.FILES.get('plantas')
        user = request.user
        username = user.username
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel)
                headers = ['Lote','Codigo','Nombre','Visible','Latitud','Longitud','Diametro']
                missing_headers = Validate_Headers_Excel(headers, df)
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
                errors = []
                for index, row in df.iterrows():
                    Id_Lote = GetIdLote(row['Lote'].strip())
                    Id_Planta = GetIdPlanta(row['Codigo'].strip())
                    if Id_Lote is None:
                        break
                    serializer_data = {
                        'Id_Lote': Id_Lote,
                        'Codigo_Planta': row['Codigo'].strip(),
                        'Nombre': row['Nombre'].strip(),
                        'Visible': True if row['Visible']==1 else False,
                        'Usuario': str(username),
                        'lat': row['Latitud'],
                        'lng': row['Longitud'],
                    }
                    if Id_Planta is None:
                        serializer = PlantaSerializers(data=serializer_data)
                    else:
                        Plantaxd = Planta.objects.get(id=Id_Planta)
                        serializer = PlantaSerializers(Plantaxd, data=serializer_data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        print("Planta registrada con exito!")
                    else:
                        print(f'Error en la fila {index+1}: {", ".join(list(serializer.errors.values())[0])}')
                        errors.append(f"Error en la fila {index+1} {row['Lote']}: {', '.join(list(serializer.errors.values())[0])}")
                if errors:
                    errors_str = '\n'.join(errors)
                    return Response(errors_str, status=status.HTTP_400_BAD_REQUEST)
                return Response('Datos cargados correctamente', status=status.HTTP_200_OK)
                
            except Exception as e:
                print(str(e))
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No se proporcionó un archivo Excel!', status=status.HTTP_400_BAD_REQUEST)


   