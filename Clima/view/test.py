# views.py
from sqlite3 import Row
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Clima.models import Daily_Indicadores
from Clima.serializer.IndicadorSerializer import DailyIndicadorSerializers

class CargarDatosDesdeExcel(APIView):
    def post(self, request):
        archivo_excel = request.FILES.get('weather')
        user = request.user
        username = user.username
        if archivo_excel:
            try:
                #df = pd.read_excel(archivo_excel)
                df = pd.read_csv(archivo_excel, skiprows=13)
                headers=["local_time","cl","ET","ETc","gdd","gdd_source","gdd_cumulative","gdd_cumulative_source",
                        "NDVI","min_rh","rh_at_max_temp","rh_at_min_temp","swdw","max_temp","mean_temp",
                        "min_temp","max_temp_dew","max_temp_time","min_temp_time","precip","precip_hours",
                        "cumulative_precip","sea_level_pressure","vapor_pressure_deficit","Kc","leaf_wetness",
                        "dew_temp","crop_water_demand","sunshine_duration","wind_direction_cardinal","wind_speed",
                        "wind_direction_degrees","wind_speed_max","wind_speed_min","wind_source"]
                missing_headers = [header for header in headers fecha_visitaif header.lower() not in [col.lower() for col in df.columns]]
                if missing_headers:
                    return Response(f'Faltan los siguientes encabezados: {", ".join(missing_headers)}', status=status.HTTP_400_BAD_REQUEST)
                
                errors = []
                print(df)
                
                for index, row in df.iterrows():
                    Fecha = row['local_time'].to_pydatetime()
                    DataRegistred = Daily_Indicadores.objects.filter(Date__month=Fecha.date().month, Date__year=Fecha.date().year,Date__day=Fecha.date().day)
                    if DataRegistred.exists():
                        print(f"{index+1} ya tiene un registro")
                        errors.append(f"Error en la fila {index+1} :Ya existe un registro para esta fecha!")
                        continue
                    
                   
                    serializer_data = {
                        "Date":row["local_time"],
                        
                        "Date_Sync":datetime.now(),
                        "Precipitacion":row["precip"],
                        
                        
                        "Precipitacion_Hours":row["precip_hours"],
                        "Ndvi":row["ndvi"], 
                        "Crop_Water_Demand":row["crop_water_demand"], 
                        "Sunshine_Duration":row["sunshine_duration"], 	
                        "Evapotranspiration":row["ET"], 
                        "Evapotranspiration_Crop":row["ETC"],	 
                        "Relat_Hum_Max":row["min_rh"], 
                        "Relat_Hum_Max":row["max_rh"], 
                        "Vapor_Pressure_Deficit":row["vapor_pressure_deficit"], 
                        "Shortwave_Downwelling":row["swdw"], 
                        "Temp_Air_Mean":row["mean_temp"],
                        "Temp_Air_Min":row["mim_temp"], 
                        "Relat_Hum_Max_Temp":row["rh_at_max_temp"], 
                        "Relat_Hum_Min_Temp":row["rh_at_min_temp"], 
                        "Temp_Air_Max":row["max_temp"], 
                        "Dew_Temp_Max":row["max_temp_dew"], 
                        "Sea_Level_Pressure":row["sea_level_pressure"], 
                        "Dew_Temp_Mean":row["dew_temp"], 
                        "Temp_Air_Max_Day":row["max_temp_time"],
                        "Temp_Air_Min_Day":row["min_temp_time"],

                    }
                    print(serializer_data)
                    serializer = DailyIndicadorSerializers( data=serializer_data)
                    if serializer.is_valid():
                        serializer.save()
                        print("Dato registrado con exito!")
                    else:
                        print(f'Error en la fila {index+1}: {", ".join(list(serializer.errors.values())[0])}')
                        errors.append(f"Error en la fila {index+1} : {', '.join(list(serializer.errors.values())[0])}")
                if errors:
                    errors_str = '\n'.join(errors)
                    return Response(errors_str, status=status.HTTP_400_BAD_REQUEST)
                return Response('Datos cargados correctamente', status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No se proporcionó un archivo Excel'}, status=status.HTTP_400_BAD_REQUEST)
