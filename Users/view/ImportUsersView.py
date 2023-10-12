from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Users.serializer.UserSerializer import UserSerializer
import pandas as pd

"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ImportUsers(APIView):
    
    def post(self, request):
        archivo_excel = request.FILES.get('usuarios')
        if archivo_excel:
            try:
                df = pd.read_excel(archivo_excel)
                for index, row in df.iterrows():
                    ###Persona.objects.create(nombre=row['nombre'], edad=row['edad'])
                    print(index)
                    print(row[0])
                return Response({'mensaje': 'Datos cargados correctamente'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No se proporcionó un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)
