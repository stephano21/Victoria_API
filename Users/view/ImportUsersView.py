from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Users.serializer.UserSerializer import UserSerializer
import pandas as pd

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ImportUsers(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'usuarios': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format='binary',
                    description='Archivo Excel con los datos de los usuarios'
                )
            }
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
        archivo_excel = request.FILES.get('usuarios')
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel)
                headers = ['Cedula','Nombre','Apellido','Usuario','Correo','Contraseña']
                missing_headers = [header for header in headers if header.lower() not in [col.lower() for col in df.columns]]
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                else:
                    errors = []
                    for index, row in df.iterrows():
                        if not all(row[col] and not pd.isna(row[col]) for col in headers):
                            missing_data = [col for col in headers if not row[col] or pd.isna(row[col])]
                            errors.append(f'Datos faltantes en la fila {index+1} : {", ".join(missing_data)}')
                            continue

                        perfil_data = {
                            'cedula': row['Cedula'],
                        }
                        
                        # Crea un serializer de usuario pasando los datos del perfil en el contexto
                        serializer_data = {
                            'username': row['Usuario'],
                            'password': row['Contraseña'],
                            'email': row['Correo'],
                            'first_name': row['Nombre'],
                            'last_name': row['Apellido'],
                        }
                        print(serializer_data)
                        serializer = UserSerializer(data=serializer_data, context={'perfil_data': perfil_data})
                        
                        if serializer.is_valid():
                            serializer.save()
                            print("Usuario registrado correctamente")
                        else:
                            errors.append(', '.join(list(serializer.errors.values())[0]))
                    if errors:
                        errors_str = f"Error en la fila {index+1} :{','.join(errors)}"
                        return Response(errors_str, status=status.HTTP_400_BAD_REQUEST)
                    
                    return Response('Datos cargados correctamente', status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                print(str(e))
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No se proporcionó un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)
