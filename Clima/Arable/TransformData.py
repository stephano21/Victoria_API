from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote
import pandas as pd


def GetData():
    queryset = Daily_Indicadores.objects.all()
    data = [{'date': obj.Date,'temp': obj.Temp_Air_Mean} for obj in queryset]

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    # Convertir la columna de fecha al formato correcto
    df['date'] = pd.to_datetime(df['date'])
    # Agrupar por mes y calcular el promedio
    df = df.groupby(df['date'].dt.to_period("M")).agg({'temp': 'mean'}).reset_index()

    df.to_dict(orient='records')    
    print(df)

def getLotes():
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote').all()
    print(queryset)
    data = [{'date': obj.FechaVisita,'lote':obj.Id_Planta.Id_Lote.Codigo_Lote ,'temp': obj.E1} for obj in queryset]
    print(data)
    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    print(df)