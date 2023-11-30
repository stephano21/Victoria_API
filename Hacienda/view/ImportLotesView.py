from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""Security"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""Models and Serializers"""
from Hacienda.models import Lote
from Hacienda.serializers import LoteSerializers
import pandas as pd
from datetime import datetime
import uuid
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Hacienda.validators.ValidatorHelper import Validate_Headers_Excel,validate_row, GetIdLote
class ImportLotesView(APIView):
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
        archivo_excel = request.FILES.get('lotes')
        user = request.user
        username = user.username
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel)
                headers = ['Lote','Variedad','Hectareas']
                missing_headers = Validate_Headers_Excel(headers, df)
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
                errors = []
                print(df)
                df['Variedad'] = df['Variedad'].fillna("-")
                df['Hectareas']= df['Hectareas'].round(2)

                for index, row in df.iterrows():
                    Id_Lote = GetIdLote(row['Lote'])
                    if Id_Lote is None:
                        break
                    print(Id_Lote)
                    row['Variedad'] = row['Variedad'] if row['Variedad'] !="nan"  else ""
                    serializer_data = {
                        'Id_Lote': Id_Lote,
                        'Hectareas': row['Hectareas'],
                        'Variedad': row['Variedad'],
                        'Usuario': str(username),
                    }
                    print(serializer_data)
                    lote = Lote.objects.get(id=Id_Lote)
                    serializer = LoteSerializers(lote, data=serializer_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        print("Lote Actualizado con exito!")
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


   