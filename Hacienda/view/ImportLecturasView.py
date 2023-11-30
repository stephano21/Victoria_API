from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""Security"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
"""Models and Serializers"""
from Hacienda.models import Lectura
from Hacienda.serializers import LecturaSerializers
import pandas as pd
from datetime import datetime
import uuid
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Hacienda.validators.ValidatorHelper import validate_row, GetIdPlanta,ValidateLectura
class ImportLecturas(APIView):
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
        archivo_excel = request.FILES.get('lecturas')
        user = request.user
        username = user.username
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel, dtype={"Observacion": str})
                headers = ['Planta','Fecha','E1','E2','E3','E4','E5','GR1','GR2','GR3','GR4','GR5','Cherelles','Total','Observacion']
                missing_headers = [header for header in headers if header.lower() not in [col.lower() for col in df.columns]]
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
                df_copy = df.copy()
                df_copy['Observacion'] = df_copy['Observacion'].astype(str)
                
                errors = []
                print(df_copy)
                save_succes = 0

                for index, row in df_copy.iterrows():
                    validate_row(row, index, errors)
                    Id_Planta = GetIdPlanta(row['Planta'])
                    if Id_Planta is None:
                        continue
                    print(Id_Planta)
                    fecha_visita = row['Fecha'].to_pydatetime()
                    lecturas_mes = Lectura.objects.filter(FechaVisita__month=fecha_visita.date().month, FechaVisita__year=fecha_visita.date().year, Id_Planta=Id_Planta)
                    if lecturas_mes.exists():
                        print(f"{row['Planta']} ya tiene una lectura")
                        errors.append(f"Error en la fila {index+1} {row['Planta']}:Ya existe una lectura de esta planta en este mes!")
                        continue
                    #row['Observacion'] = row['Observacion'].fillna("")
                    row['Observacion'] = row['Observacion'] if row['Observacion'] !="nan"  else ""
                    # Crea un serializer de usuario pasando los datos del perfil en el contexto
                    serializer_data = {
                        'Id_Planta': Id_Planta,
                        'FechaVisita': fecha_visita,
                        'E1': row['E1'],
                        'E2': row['E2'],
                        'E3': row['E3'],
                        'E4': row['E4'],
                        'E5': row['E5'],
                        'GR1': row['GR1'],
                        'GR2': row['GR2'],
                        'GR3': row['GR3'],
                        'GR4': row['GR4'],
                        'GR5': row['GR5'],
                        'Cherelles': row['Cherelles'],
                        'Total': row['Total'],
                        'Observacion': row['Observacion'] if not pd.isna(row['Observacion']) else "",
                        'Monilla': row['Monilla'] ,
                        'Usuario': str(username),
                        'SyncId': str(uuid.uuid4()),
                        'GUIDLectura':uuid.uuid4,
                    }
                    #print(serializer_data)
                    validate = ValidateLectura(serializer_data)
                    if validate != "":
                        return Response(validate, status=status.HTTP_400_BAD_REQUEST)
                    serializer = LecturaSerializers(data=serializer_data)
                    #print(serializer)
                    if serializer.is_valid():
                        serializer.save()
                        save_succes+=1
                        print("Lectura  registrada exitosamente!")
                    else:
                        #print(f'Error en la fila {index+1}: {", ".join(list(serializer.errors.values())[0])}')
                        errors.append(f"Error en la fila {index+1} {row['Planta']}: {', '.join(list(serializer.errors.values())[0])}")
                if errors:
                    errors_str = '\n'.join(errors)
                    return Response(errors_str+f'\nse han cargado {save_succes} correctamente', status=status.HTTP_400_BAD_REQUEST)
                return Response(f'se han cargado {save_succes} correctamente', status=status.HTTP_200_OK)
                
            except Exception as e:
                print(str(e))
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No se proporcionó un archivo Excel!', status=status.HTTP_400_BAD_REQUEST)


   