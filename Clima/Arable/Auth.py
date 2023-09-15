from datetime import datetime, timedelta

import requests
from decouple import config
#models
from Clima.models import Daily_Indicadores

def Login():
    if 1==2:
        return config('ARABLE_TOKEN')
    url = config('ARABLE_API')
    if not isinstance(url, str):
        raise ValueError("La url no se ha proporcionado")
    """ headers = {
        'Authorization': 'Bearer YOUR_JWT_TOKEN',
    } """

    data = {
        'email': config('A_EMAIL'),
        'password': config('A_PASSWORD'),
    }

    response = requests.post(url, json=data)
    # Almacenar el token en una variable de entorno si la respuesta es exitosa
    if response.status_code == 200:
        data_from_api = response.json()
        return data_from_api["token"]
    else:
        return ""

def Current_Date():
    try:
        latest_date = Daily_Indicadores.objects.latest('Date').Date
        return datetime.combine(latest_date, datetime.min.time())
    except Exception as e:
        return None

def Current_Data():
    try:
        ultimo_registro = Current_Date()
        fecha_actual = datetime.now()
        if ultimo_registro is not None and ultimo_registro is not None:
            if ultimo_registro.date() == fecha_actual.date():
                return True
        return False
    except Exception as e:
        print(str(e))
        return False
#no lo uso DRF hace el formateo
def Format_Local_Date(fecha_utc):
    try:
        fecha_formato = datetime.strptime(fecha_utc, "%Y-%m-%d %H:%M:%S%z")
    except ValueError:
        try:
            fecha_formato = datetime.strptime(fecha_utc, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            fecha_formato = datetime.strptime(fecha_utc, "%Y-%m-%d %H:%M:%S+00")
    fecha_guayaquil = fecha_formato - timedelta(hours=5)
    return fecha_guayaquil


def GetData(token, start_time=None):
    # Crear la URL dinámicamente
    device = config('ARABLE_DEVICE')
    temp = config('ARABLE_TEMP')
    end_time = datetime.now().date() #"2023-09-11"
    
    params = f"?device={device}&end_time={end_time}&temp={temp}"
    url = config('ARABLE_DATA')
    if not isinstance(url, str) and not isinstance(device, str) and not isinstance(temp, str):
        raise ValueError("La url no se ha proporcionado")

    if start_time is not None:
        print(start_time)
        start_time += timedelta(days=1)
        params += f"&start_time={start_time}"
    else:
        start_time = "2022-09-11"
        print(start_time)
        params += f"&start_time={start_time}"
    print(params)

    url = str(url) + params
    headers = {
        'Authorization': f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)  
    if response.status_code == 200:
        data_from_api = response.json()
        return response.json()
    else:
        return ""
def BuidlSerializer(data,user):
    Serializer_Arrya=[]
    try:
        for sense in data:
            object={
                "Date":sense["time"],
                "Date_Arable_Sync":sense["update_time"],
                "Date_Sync":datetime.now(),
                "Lat":sense["lat"],
                "Lng":sense["long"],
                "LocationID":sense["location"],
                "Device":sense["device"],
                "Precipitacion":sense["precip"],
                "Precipitacion_Hours":sense["precip_hours"],
                "Temp_Air_Mean":sense["meant"],
                "Temp_Air_Min":sense["maxt"], 
                "Temp_Air_Max":sense["mint"], 
                "Temp_Air_Max_Day":sense["maxt_time"],
                "Temp_Air_Min_Day":sense["mint_time"],
                "Temp_Below":sense["lfairdelta"], 
                "Temp_Below_Mean":sense["mean_tbelow"], 
                "Dew_Temp_Mean":sense["tdew"], 
                "Dew_Temp_Max":sense["max_tdew"], 
                "Dew_Temp_At_Min_Temp":sense["tdew_at_mint"], 
                "Ndvi":sense["ndvi"], 
                "Evapotranspiration":sense["et"], 
                "Evapotranspiration_Crop":sense["etc"],	 
                "Relat_Hum_Mean":sense["mean_rh"], 
                "Relat_Hum_Min":sense["max_rh"], 
                "Relat_Hum_Max":sense["min_rh"], 
                "Relat_Hum_Max_Temp":sense["rh_at_maxt"], 
                "Relat_Hum_Min_Temp":sense["rh_at_mint"], 
                "Crop_Water_Demand":sense["crop_water_demand"], 
                "Sunshine_Duration":sense["sunshine_duration"], 	
                "Dli":sense["dli"],
                "Sea_Level_Pressure":sense["slp"], 
                "Vapor_Pressure":sense["ea"], 
                "Vapor_Pressure_Deficit":sense["vpd"], 
                "Shortwave_Downwelling":sense["swdw"], 
                "Activo":True,
                "Usuario":user,
            }
            Serializer_Arrya.append(object)
        return Serializer_Arrya
    except Exception as e:
        return str(e)
