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
                headers=["time","update_time","lat","long","location","device","precip","precip_hours","meant","maxt","mint","maxt_time","mint_time","lfairdelta","mean_tbelow","tdew","max_tdew","tdew_at_mint","ndvi","et","etc","mean_rh","max_rh","min_rh","rh_at_maxt","rh_at_mint","crop_water_demand","sunshine_duration","dli","slp","ea","vpd","swdw"]
                missing_headers = [header for header in headers if header.lower() not in [col.lower() for col in df.columns]]
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
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
