from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote,Proyecto, Produccion
import pandas as pd


def GetData():
    queryset = Daily_Indicadores.objects.all()
    data = [{'date': obj.Date,
             'temp': obj.Temp_Air_Mean, 
             'Evapotranspiration':obj.Evapotranspiration,
             'Evapotranspiration_Crop':obj.Evapotranspiration_Crop,
             'Nvdi': obj.Ndvi,
             'Relat_Hum_Min':obj.Relat_Hum_Min,
             'Relat_Hum_Max_Temp':obj.Relat_Hum_Max_Temp,
             'Relat_Hum_Max_Temp':obj.Relat_Hum_Min_Temp,
             'Temp_Air_Max':obj.Temp_Air_Max,
             'Temp_Air_Min':obj.Temp_Air_Min,
             'Dew_Temp_Max':obj.Dew_Temp_Max,
             'Precipitacion':obj.Precipitacion,
             'Precipitacion_Hours':obj.Precipitacion_Hours,
             'Sea_Level_Pressure': obj.Sea_Level_Pressure,
             'Vapor_Pressure_Deficit':obj.Vapor_Pressure_Deficit,
             'Dew_Temp_Mean':obj.Dew_Temp_Mean,
             'Crop_Water_Demand':obj.Crop_Water_Demand,
             'Sunshine_Duration':obj.Sunshine_Duration,
             } for obj in queryset]

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    # Convertir la columna de fecha al formato correcto
    df['date'] = pd.to_datetime(df['date'])
    # Agrupar por mes y calcular el promedio
    df = df.groupby(df['date'].dt.to_period("M")).agg({'temp': 'mean',
                                                       'Nvdi':'mean',
                                                       'temp':'mean',
                                                        'Evapotranspiration':'mean',
                                                        'Evapotranspiration_Crop':'mean',
                                                        'Nvdi':'mean',
                                                        'Relat_Hum_Min':'mean',
                                                        'Relat_Hum_Max_Temp':'mean',
                                                        'Relat_Hum_Max_Temp':'mean',
                                                        'Temp_Air_Max':'mean',
                                                        'Temp_Air_Min':'mean',
                                                        'Dew_Temp_Max':'mean',
                                                        'Precipitacion':'mean',
                                                        'Precipitacion_Hours':'mean',
                                                        'Sea_Level_Pressure':'mean',
                                                        'Vapor_Pressure_Deficit':'mean',
                                                        'Dew_Temp_Mean':'mean',
                                                        'Crop_Water_Demand':'mean',
                                                        'Sunshine_Duration':'mean'}).reset_index()

    df.to_dict(orient='records')    
    print(df)
    return df
def getProduction():
    queryset = Produccion.objects.select_related('Id_Proyecto__Id_Hacienda').filter(Activo=True, Id_Proyecto__Id_Hacienda_id=1)

    data = [
        {
            'date': obj.Fecha,
            'qq': obj.Qq,
            'Proyecto': obj.Id_Proyecto.Codigo_Proyecto,
        }
        for obj in queryset
    ]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby([df['date'].dt.to_period("M"), df['Proyecto']])['qq'].sum().reset_index()
    print(df)
    return df

def getLotes():
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(Activo=True, Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=1)

    data = [
        {
            'date': obj.FechaVisita,
            'producion_real': obj.Id_Planta.Id_Lote.Id_Proyecto.Codigo_Proyecto if obj.Id_Planta and obj.Id_Planta.Id_Lote and  obj.Id_Planta.Id_Lote.Id_Proyecto else None,
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'hectareas': obj.Id_Planta.Id_Lote.Hectareas,
            'densidad': obj.Id_Planta.Id_Lote.Id_Proyecto.Densidad,
            'E1': obj.E1,
            'E2': obj.E2,
            'E3': obj.E3,
            'E4': obj.E4,
            'E5': obj.E5
        } 
        for obj in queryset
    ]

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    # Agrupar por fecha y lote, calcular la media de las columnas E1-E5
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'], df['densidad'], df['hectareas']])[['E1', 'E2', 'E3', 'E4', 'E5']].mean().reset_index()
    dfByLote = df.copy()
    # Dividir la columna 'lote' en dos basado en el caracter "_"
    split_data = dfByLote['lote'].str.split('_', expand=True)
    # Renombrar las columnas del DataFrame resultante
    split_data.columns = ['Proyecto', 'Lote','xd']
    #print(split_data)
    # Concatenar el DataFrame resultante con el DataFrame original
    dfByLote = pd.concat([dfByLote, split_data], axis=1)
    # Concatenar las dos columnas usando str.cat()
    dfByLote['Proyecto'] = dfByLote['Proyecto'].str.cat(dfByLote['Lote'], sep='_')
   # print(dfByLote)

    # Agrupar por fecha y proyecto, calcular la suma de las columnas E1-E5
    dfByLote = dfByLote.groupby(['date', 'Proyecto','densidad']).agg({'hectareas':'sum','E1': 'mean', 'E2': 'mean', 'E3': 'mean', 'E4': 'mean', 'E5': 'mean'}).reset_index()
    df_Production = getProduction()
    df_Lote_Produccion =pd.merge(dfByLote, df_Production, on=['date','Proyecto'], how='inner')


    # Guardar el DataFrame en un archivo Excel
    # Convertir las columnas relevantes a tipo float
    df_Lote_Produccion['E1'] = df_Lote_Produccion['E1'].astype(float)
    df_Lote_Produccion['E2'] = df_Lote_Produccion['E1'].astype(float)
    df_Lote_Produccion['E3'] = df_Lote_Produccion['E1'].astype(float)
    df_Lote_Produccion['E4'] = df_Lote_Produccion['E1'].astype(float)
    df_Lote_Produccion['E5'] = df_Lote_Produccion['E1'].astype(float)
    df_Lote_Produccion['densidad'] = df_Lote_Produccion['densidad'].astype(float)
    df_Lote_Produccion['hectareas'] = df_Lote_Produccion['hectareas'].astype(float)
    #Aqui convierto los totales de mazorcas a quintales secos 
    df_Lote_Produccion['Total_E1']= ((df_Lote_Produccion['E1']*df_Lote_Produccion['densidad']*df_Lote_Produccion['hectareas'])/12)/100
    df_Lote_Produccion['Total_E2']= ((df_Lote_Produccion['E2']*df_Lote_Produccion['densidad']*df_Lote_Produccion['hectareas'])/12)/100
    df_Lote_Produccion['Total_E3']= ((df_Lote_Produccion['E3']*df_Lote_Produccion['densidad']*df_Lote_Produccion['hectareas'])/12)/100
    df_Lote_Produccion['Total_E4']= ((df_Lote_Produccion['E4']*df_Lote_Produccion['densidad']*df_Lote_Produccion['hectareas'])/12)/100
    df_Lote_Produccion['Total_E5']= ((df_Lote_Produccion['E5']*df_Lote_Produccion['densidad']*df_Lote_Produccion['hectareas'])/12)/100
    #Limpiar el dataset
    df_Lote_Produccion = df_Lote_Produccion.drop(['E1','E2','E3','E4','E5','densidad','hectareas'], axis=1)
    #merge with clima
    df_weather = GetData()
    df_merged_inner = pd.merge(df_Lote_Produccion, df_weather, on='date', how='inner')
    df_merged_inner.to_csv('Clima.csv', index=False)



    # Agrupar por mes y sumar
    df_Total = df_Lote_Produccion.groupby(['date']).agg({'Total_E1':'sum','Total_E2':'sum','Total_E3':'sum','Total_E4':'sum','Total_E5':'sum','qq':'sum'})
    
    #merge clima
   
    df_merged_inner.to_csv('FInalDataSet.csv', index=False)

    # Imprimir el DataFrame
   
    # Devolver los datos como un diccionario orientado a registros
    #print(df_final)
    return df.to_dict(orient='records')
 