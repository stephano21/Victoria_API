from Hacienda.validators.ValidatorHelper import Validate_Headers_Excel, validate_row, GetIdLote
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import uuid
from datetime import datetime
import pandas as pd
from Hacienda.serializers import ProduccionSerializers
from Hacienda.models import Produccion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""Security"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""Models and Serializers"""
"""Document by SWAGGER"""


class ImportProduccion(APIView):
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
        archivo_excel = request.FILES.get('produccion')
        user = request.user
        username = user.username
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel)
                headers = ['Lote', 'Fecha', 'Quintales']
                missing_headers = Validate_Headers_Excel(headers, df)
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                df['Quintales'] = df['Quintales'].round(3)
                df_copy = df.copy()

                errors = []
                print(df_copy)
                for index, row in df_copy.iterrows():
                    Id_Lote = GetIdLote(row['Lote'])
                    fecha = row['Fecha'].to_pydatetime().date()
                    if Id_Lote is None:
                        break
                    print(Id_Lote)
                    Produccion_mes = Produccion.objects.filter(
                        Fecha__month=fecha.month, Fecha__year=fecha.year, Id_Lote=Id_Lote)
                    if Produccion_mes.exists():
                        print(f"{row['Lote']} ya tiene una Produccion")
                        errors.append(
                            f"Error en la fila {index+1} {row['Lote']}:Ya existe una Produccion registrada en este mes!")
                        continue
                    # Crea un serializer de usuario pasando los datos del perfil en el contexto
                    serializer_data = {
                        'Id_Lote': Id_Lote,
                        'Fecha': fecha,
                        'Qq': row['Quintales'],
                        'Usuario': str(username),
                    }
                    print(serializer_data)
                    serializer = ProduccionSerializers(data=serializer_data)
                    # print(serializer)
                    if serializer.is_valid():
                        serializer.save()
                        print("Producción  registrada exitosamente!")
                    else:
                        # print(f'Error en la fila {index+1}: {", ".join(list(serializer.errors.values())[0])}')
                        errors.append(
                            f"Error en la fila {index+1} {row['Lote']}: {', '.join(list(serializer.errors.values())[0])}")
                if errors:
                    errors_str = '\n'.join(errors)
                    return Response(errors_str, status=status.HTTP_400_BAD_REQUEST)
                return Response('Datos cargados correctamente', status=status.HTTP_200_OK)

            except Exception as e:
                print(str(e))
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No se proporcionó un archivo Excel!', status=status.HTTP_400_BAD_REQUEST)
