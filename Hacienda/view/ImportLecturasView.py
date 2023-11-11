from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models  import User
from Users.models import Perfil
from Users.serializer.UserSerializer import UserSerializer
import pandas as pd

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ImportLecturas(APIView):
    
    def validate_row(self,row, index, errors,headers):
        has_error = False
        if not all(row[col] and not pd.isna(row[col]) for col in headers):
            missing_data = [col for col in headers if not row[col] or pd.isna(row[col])]
            errors.append(f'Datos faltantes en la fila {index+1} : {", ".join(missing_data)}')
            has_error = True
        
        cedula = row['Cedula']
        if len(str(cedula)) != 10 and has_error == False:
            errors.append(f"Error en la fila {index+1} {row['Usuario']}: El numero de cedula es incorrecto!")
            has_error = True
        if len(str(row['Usuario']))<=3 and has_error == False:
            errors.append(f"Error en la fila {index+1} : El Nombre de usuario es inválido")
            has_error = True
        if User.objects.filter(username=row['Usuario']).exists() and has_error == False:
            errors.append(f"Error en la fila {index+1} {row['Usuario']}: El Usuario ya está registrado!")
            has_error = True
        # Validar que el campo 'cedula' no exista en el modelo Perfil
        if Perfil.objects.filter(cedula=cedula).exists() and has_error == False:
            errors.append(f"Error en la fila {index+1} {row['Usuario']}: El numero de cedula ya está registrado!")
            has_error = True
        if has_error:
            return errors
        return
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
        archivo_excel = request.FILES.get('usuarios')
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel, dtype={"Cedula": str})
                headers = ['Cedula','Nombre','Apellido','Usuario','Correo','Contraseña']
                missing_headers = [header for header in headers if header.lower() not in [col.lower() for col in df.columns]]
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
                df_copy = df.copy()
                df_copy['mi_columna'] = df_copy['Cedula'].astype(str)
                
                errors = []
                print(df_copy)
                for index, row in df_copy.iterrows():
                    self.validate_row(row, index, errors,headers)
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
                        print(f'Error en la fila {index+1}: {", ".join(list(serializer.errors.values())[0])}')
                        errors.append(f"Error en la fila {index+1} {row['Usuario']}: {', '.join(list(serializer.errors.values())[0])}")
                if errors:
                    errors_str = '\n'.join(errors)
                    return Response(errors_str, status=status.HTTP_400_BAD_REQUEST)
                return Response('Datos cargados correctamente', status=status.HTTP_200_OK)
                
            except Exception as e:
                print(str(e))
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No se proporcionó un archivo Excel!', status=status.HTTP_400_BAD_REQUEST)


   