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
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote').filter(Activo=True,)
   # print(queryset)

    data = [
        {
            'date': obj.FechaVisita,
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'E1': obj.E1,
            'E2': obj.E2,
            'E3': obj.E3,
            'E4': obj.E4,
            'E5': obj.E5
        } 
        for obj in queryset
    ]
    #print(data)

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    df = df.groupby([df['date'].dt.to_period("M"), df['lote']])[['E1','E2','E3','E4','E5']].mean().reset_index()
    df.to_excel('Estimaciones.xlsx', index=False)


    df.to_dict(orient='records')    

    print(df)