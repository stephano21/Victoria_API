from Clima.Arable.Auth import GetData, Login, BuidlSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Clima.models import Daily_Indicadores
from Clima.serializers import DailyIndicadorSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.Console import console
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pandas as pd
"""
Arable data
"""


class DataView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Data = Daily_Indicadores.objects
        serializer = Daily_Indicadores.objects.filter(Activo=True).order_by('Date')
        data = [
            {
                "Date": obj.Date,
                "Date_Arable_Sync": obj.Date_Arable_Sync,
                "Date_Sync": obj.Date_Sync,
                "Lat": obj.Lat,
                "Lng": obj.Lng,
                "LocationID": obj.LocationID,
                "Device": obj.Device,
                "Precipitacion": obj.Precipitacion,
                "Precipitacion_Hours": obj.Precipitacion_Hours,
                "Temp_Air_Mean": obj.Temp_Air_Mean,
                "Temp_Air_Min": obj.Temp_Air_Min,
                "Temp_Air_Max": obj.Temp_Air_Max,
                "Temp_Air_Max_Day": obj.Temp_Air_Max_Day,
                "Temp_Air_Min_Day": obj.Temp_Air_Min_Day,
                "Temp_Below": obj.Temp_Below,
                "Temp_Below_Mean": obj.Temp_Below_Mean,
                "Dew_Temp_Mean": obj.Dew_Temp_Mean,
                "Dew_Temp_Max": obj.Dew_Temp_Max,
                "Dew_Temp_At_Min_Temp": obj.Dew_Temp_At_Min_Temp,
                "Ndvi": obj.Ndvi,
                "Evapotranspiration": obj.Evapotranspiration,
                "Evapotranspiration_Crop": obj.Evapotranspiration_Crop,
                "Relat_Hum_Mean": obj.Relat_Hum_Mean,
                "Relat_Hum_Min": obj.Relat_Hum_Min,
                "Relat_Hum_Max": obj.Relat_Hum_Max,
                "Relat_Hum_Max_Temp": obj.Relat_Hum_Max_Temp,
                "Relat_Hum_Min_Temp": obj.Relat_Hum_Min_Temp,
                "Crop_Water_Demand": obj.Crop_Water_Demand,
                "Sunshine_Duration": obj.Sunshine_Duration,
                "Dli": obj.Dli,
                "Sea_Level_Pressure": obj.Sea_Level_Pressure,
                "Vapor_Pressure": obj.Vapor_Pressure,
                "Vapor_Pressure_Deficit": obj.Vapor_Pressure_Deficit,
                "Shortwave_Downwelling": obj.Shortwave_Downwelling,
                "Activo": obj.Activo,
                "Usuario": obj.Usuario,
            }
            for obj in serializer
        ]
        serializer = {
            "data": data,
            "analytics":self.GroupedData(data)
        }
        
        return Response(serializer, status=status.HTTP_200_OK)

    def GroupedData(self, data):
        df = pd.DataFrame(data)
        df = df.groupby(df['Date'].dt.to_period("M")).agg({
            'Evapotranspiration_Crop': 'sum',
            'Ndvi': 'sum',
            'Relat_Hum_Max_Temp': 'mean',
            'Temp_Air_Max': 'mean',
            'Temp_Air_Min': 'mean',
            'Dew_Temp_Max': 'mean',
            'Precipitacion': 'sum',
            'Sunshine_Duration': 'sum'
        }).reset_index()
        df['Date'] = df['Date'].astype(str) + "-01"
        
        grouped_data = df.to_dict(orient='records')
        
        console.log(grouped_data)
        return grouped_data
