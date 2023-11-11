# views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CargarDatosDesdeExcel(APIView):
    def post(self, request, format=None):
        archivo_excel = request.FILES.get('data')
        if archivo_excel:
            try:
                #df = pd.read_excel(archivo_excel)
                df = pd.read_csv(archivo_excel, skiprows=13)
                print(df)
                for index, row in df.iterrows():
                    ###Persona.objects.create(nombre=row['nombre'], edad=row['edad'])
                    #print(index)
                    #print(row)
                    pass
                return Response({'mensaje': 'Datos cargados correctamente'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No se proporcionó un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)
