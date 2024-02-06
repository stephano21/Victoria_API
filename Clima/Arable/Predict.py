from django.db.models import Avg, Sum
from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote, Proyecto, Produccion
import pandas as pd
# Sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, accuracy_score, median_absolute_error, r2_score
import re  # Expreciones regulares
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd


def get_column_value(df, date, column_name, months_ago, lote):
    # Convertir la fecha hace "months_ago" meses a datetime
    target_date = pd.to_datetime(date - relativedelta(months=months_ago))

    # Filtrar el DataFrame original para obtener el valor correspondiente a la fecha
    filtered_data = df[(df['date'] == target_date) & (df['lote'] == lote)]

    # Obtener el valor de la columna deseada
    if not filtered_data.empty:
        return filtered_data.iloc[0][column_name]
    else:
        return 0            

def get_column_valuev2(df, date, column_name, months_ago, lotestr,hacienda):
    # Convertir la fecha hace "months_ago" meses a datetime
    #target_date = pd.to_datetime(date - relativedelta(months=months_ago))
     # Obtener la fecha hace "months_ago" meses
    print(f"{date},{lotestr} meses a tras{months_ago} Estadio{column_name}")
    target_date = date.to_timestamp() - pd.DateOffset(months=months_ago)
    print(target_date)
    # Obtener el último día del mes de target_date
    last_day_of_month = target_date + pd.offsets.MonthEnd(0)
    print(last_day_of_month)

   
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True, 
        Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda, 
        Id_Planta__Id_Lote__Codigo_Lote =lotestr,  
        FechaVisita__gte=target_date,
        FechaVisita__lte=last_day_of_month,)

    data = [
        {
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote,
            f'{column_name}': getattr(obj, column_name),
        }
        for obj in queryset
    ]
    dfRetorno=pd.DataFrame(data)
    print(dfRetorno)


    # Obtener el valor de la columna deseada
    
    if len(dfRetorno)>0:
        dfRetorno = dfRetorno.groupby([dfRetorno['lote']])[[column_name]].sum().reset_index()
        return int(dfRetorno[column_name].iloc[0])
    else:
        return 0

def GetLecturas(hacienda):
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True, Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
    data = []
    for obj in queryset:
        lectura_data = {
            'date': obj.FechaVisita,
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'edad': obj.Id_Planta.Id_Lote.Edad,
            'Cherelles': obj.Cherelles,
            'E1': obj.E1,
            'E2': obj.E2,
            'E3': obj.E3,
            'E4': obj.E4,
            'E5': obj.E5,
            'GR1': obj.GR1,
            'GR2': obj.GR2,
            'GR3': obj.GR3,
            'GR4': obj.GR4,
            'GR5': obj.GR5,
        }

        weather_data = get_weather_for_date(obj.FechaVisita)
        lectura_data.update(weather_data)

        data.append(lectura_data)
    df = pd.DataFrame(data)
    # Calcular las columnas E1, E2, E3 de hace 3, 2, 1 meses respectivamente
    for i in range(1, 4):
        df[f'E{i}'] = df.apply(
            lambda row: get_column_value(df, row['date'], f'E{i}', i, row['lote']), axis=1)
    print(df)
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'], df ['edad']])[
        ['E1', 'E2', 'E3', 'E4', 'E5', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5', 'Cherelles','temp','Evapotranspiration','Evapotranspiration_Crop','Nvdi','Relat_Hum_Min','Relat_Hum_Max_Temp','Relat_Hum_Min_Temp','Temp_Air_Max','Temp_Air_Min','Dew_Temp_Max','Precipitacion','Precipitacion_Hours','Sea_Level_Pressure','Vapor_Pressure_Deficit','Dew_Temp_Mean','Crop_Water_Demand','Sunshine_Duration']].sum().reset_index()
    # Seleccionar solo las columnas objetivo
    target_columns = df.loc[:, 'GR1':'GR5']
    # Obtener la columna con el mayor valor en cada fila en el rango específico
    max_column = target_columns.idxmax(axis=1)

    # Asignar un número según la posición de la columna
    df['grade_monilla'] = max_column.str.extract('(\d+)')
    df = df.drop(['GR1', 'GR2', 'GR3', 'GR4', 'GR5'], axis=1)
    # df.to_excel('output.xlsx', index=False)
    # Convertir los datos a DataFrame de pandas
    df.to_excel("tesssss.xlsx", index=False)
    return df


def get_weather_for_date(date):
    print("Gett weather")
    # Obtener la fecha hace 3 meses
    three_months_ago = date - relativedelta(months=3)

    # Obtener el primer día del mes hace 3 meses
    first_day_of_three_months_ago = three_months_ago.replace(day=1)

    # Obtener los datos climáticos para el mes específico hace 3 meses
    queryset = Daily_Indicadores.objects.filter(
        Date__gte=first_day_of_three_months_ago, Date__lt=date)

    if not queryset.exists():
        return {
            'temp': 0,
            'Evapotranspiration': 0,
            'Evapotranspiration_Crop': 0,
            'Nvdi': 0,
            'Relat_Hum_Min': 0,
            'Relat_Hum_Max_Temp': 0,
            'Relat_Hum_Min_Temp': 0,
            'Temp_Air_Max': 0,
            'Temp_Air_Min': 0,
            'Dew_Temp_Max': 0,
            'Precipitacion': 0,
            'Precipitacion_Hours': 0,
            'Sea_Level_Pressure': 0,
            'Vapor_Pressure_Deficit': 0,
            'Dew_Temp_Mean': 0,
            'Crop_Water_Demand': 0,
            'Sunshine_Duration': 0,
        }

    # Calcular el promedio para la temperatura y la suma para otros parámetros
    avg_temp = queryset.aggregate(avg_temp=Avg('Temp_Air_Mean'))['avg_temp']
    total_evapotranspiration = queryset.aggregate(
        sum_evapotranspiration=Sum('Evapotranspiration'))['sum_evapotranspiration']
    # Otros campos...

    return {
        'temp': avg_temp,
        'Evapotranspiration': total_evapotranspiration,
        'Evapotranspiration_Crop': queryset.aggregate(sum_evapotranspiration_crop=Sum('Evapotranspiration_Crop'))['sum_evapotranspiration_crop'],
        'Nvdi': queryset.aggregate(sum_nvdi=Sum('Ndvi'))['sum_nvdi'],
        'Relat_Hum_Min': queryset.aggregate(avg_relat_hum_min=Avg('Relat_Hum_Min'))['avg_relat_hum_min'],
        'Relat_Hum_Max_Temp': queryset.aggregate(avg_relat_hum_max_temp=Avg('Relat_Hum_Max_Temp'))['avg_relat_hum_max_temp'],
        'Relat_Hum_Min_Temp': queryset.aggregate(avg_relat_hum_min_temp=Avg('Relat_Hum_Min_Temp'))['avg_relat_hum_min_temp'],
        'Temp_Air_Max': queryset.aggregate(max_temp_air_max=Avg('Temp_Air_Max'))['max_temp_air_max'],
        'Temp_Air_Min': queryset.aggregate(min_temp_air_min=Avg('Temp_Air_Min'))['min_temp_air_min'],
        'Dew_Temp_Max': queryset.aggregate(max_dew_temp_max=Avg('Dew_Temp_Max'))['max_dew_temp_max'],
        'Precipitacion': queryset.aggregate(sum_precipitacion=Sum('Precipitacion'))['sum_precipitacion'],
        'Precipitacion_Hours': queryset.aggregate(sum_precipitacion_hours=Sum('Precipitacion_Hours'))['sum_precipitacion_hours'],
        'Sea_Level_Pressure': queryset.aggregate(avg_sea_level_pressure=Avg('Sea_Level_Pressure'))['avg_sea_level_pressure'],
        'Vapor_Pressure_Deficit': queryset.aggregate(avg_vapor_pressure_deficit=Avg('Vapor_Pressure_Deficit'))['avg_vapor_pressure_deficit'],
        'Dew_Temp_Mean': queryset.aggregate(avg_dew_temp_mean=Avg('Dew_Temp_Mean'))['avg_dew_temp_mean'],
        'Crop_Water_Demand': queryset.aggregate(sum_crop_water_demand=Sum('Crop_Water_Demand'))['sum_crop_water_demand'],
        'Sunshine_Duration': queryset.aggregate(sum_sunshine_duration=Sum('Sunshine_Duration'))['sum_sunshine_duration'],
    }


def getProduction(hacienda):
    queryset = Produccion.objects.select_related('Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True, Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)

    data = [
        {
            'date': obj.Fecha,
            'qq': obj.Qq,
            'lote': obj.Id_Lote.Codigo_Lote,
            'edad': obj.Id_Lote.Edad,
        }
        for obj in queryset
    ]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'], df['edad']])[
        'qq'].sum().reset_index()
    df.to_excel("ProduccionDF.xlsx", index=False)
    return df
def GetLecturasv1(hacienda):
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True, Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
    data = []
    for obj in queryset:
        lectura_data = {
            'date': obj.FechaVisita,
            'Id_Lote': obj.Id_Planta.Id_Lote,
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'edad': obj.Id_Planta.Id_Lote.Edad,
            'Cherelles': obj.Cherelles,
            'E1': obj.E1,
            'E2': obj.E2,
            'E3': obj.E3,
            'E4': obj.E4,
            'E5': obj.E5,
            'GR1': obj.GR1,
            'GR2': obj.GR2,
            'GR3': obj.GR3,
            'GR4': obj.GR4,
            'GR5': obj.GR5,
        }
        data.append(lectura_data)
    df = pd.DataFrame(data)
    # Calcular las columnas E1, E2, E3 de hace 3, 2, 1 meses respectivamente
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'],df['Id_Lote'], df ['edad']])[
        ['E1', 'E2', 'E3', 'E4', 'E5', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5', 'Cherelles']].sum().reset_index()
    # Seleccionar solo las columnas objetivo
    target_columns = df.loc[:, 'GR1':'GR5']
    # Obtener la columna con el mayor valor en cada fila en el rango específico
    max_column = target_columns.idxmax(axis=1)

    # Asignar un número según la posición de la columna
    df['grade_monilla'] = max_column.str.extract('(\d+)')
    df = df.drop(['GR1', 'GR2', 'GR3', 'GR4', 'GR5'], axis=1)
    print(df)

    # df.to_excel('output.xlsx', index=False)
    # Convertir los datos a DataFrame de pandas
    #df.to_excel("tesssss.xlsx", index=False)
    return df

def GetWeather():
    queryset = Daily_Indicadores.objects.all()
    data = [{'date': obj.Date,
             'temp': obj.Temp_Air_Mean,
             'Evapotranspiration': obj.Evapotranspiration,
             'Evapotranspiration_Crop': obj.Evapotranspiration_Crop,
             'Nvdi': obj.Ndvi,
             'Relat_Hum_Min': obj.Relat_Hum_Min,
             'Relat_Hum_Max_Temp': obj.Relat_Hum_Max_Temp,
             'Relat_Hum_Min_Temp': obj.Relat_Hum_Min_Temp,
             'Temp_Air_Max': obj.Temp_Air_Max,
             'Temp_Air_Min': obj.Temp_Air_Min,
             'Dew_Temp_Max': obj.Dew_Temp_Max,
             'Precipitacion': obj.Precipitacion,
             'Precipitacion_Hours': obj.Precipitacion_Hours,
             'Sea_Level_Pressure': obj.Sea_Level_Pressure,
             'Vapor_Pressure_Deficit': obj.Vapor_Pressure_Deficit,
             'Dew_Temp_Mean': obj.Dew_Temp_Mean,
             'Crop_Water_Demand': obj.Crop_Water_Demand,
             'Sunshine_Duration': obj.Sunshine_Duration,
             } for obj in queryset]

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(data)
    # Asegurarse de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Restar 3 meses a la columna 'date'
    df['date'] = df['date'] + pd.DateOffset(months=3)

    # Hacer el ajuste de fin de mes después de restar 3 meses
    df['date'] = df['date'] + MonthEnd(0)
    df = df.groupby(df['date'].dt.to_period("M")).agg({'temp': 'mean',
                                                       'Evapotranspiration': 'sum',
                                                       'Evapotranspiration_Crop': 'sum',
                                                       'Nvdi': 'sum',
                                                       'Relat_Hum_Min': 'mean',
                                                       'Relat_Hum_Max_Temp': 'mean',
                                                       'Temp_Air_Max': 'mean',
                                                       'Temp_Air_Min': 'mean',
                                                       'Dew_Temp_Max': 'mean',
                                                       'Precipitacion': 'sum',
                                                       'Precipitacion_Hours': 'sum',
                                                       'Sea_Level_Pressure': 'mean',
                                                       'Vapor_Pressure_Deficit': 'mean',
                                                       'Dew_Temp_Mean': 'mean',
                                                       'Crop_Water_Demand': 'sum',
                                                       'Sunshine_Duration': 'sum'}).reset_index()

    df.to_dict(orient='records')
    df.to_excel("DatosClimaticos.xlsx", index=False)
    return df


def GenerateDF(hacienda):
    dfLecturas = GetLecturasv1(hacienda)
    dfProduction = getProduction(hacienda)
    print(dfProduction)
    dfWeather = GetWeather()
   # Hacer merge entre dfLecturas y dfProduction usando how='right'
    df_merged = pd.merge(dfLecturas, dfProduction, on=['date', 'lote','edad'], how='right')
    df_merged = df_merged.fillna(0)
    # Hacer merge con dfWeather usando 'date'
    df_final = pd.merge(df_merged, dfWeather, on='date', how='inner')
    for i in range(3, 0, -1):
        df_final[f'E{4-i}'] = df_final.apply(
            lambda row: get_column_valuev2(df_final, row['date'], f'E{4-i}', i, row['lote'],hacienda), axis=1)
    
    print(df_final)
    # df.to_csv('Clima.csv', index=False)
    # df.to_excel('DFNew.xlsx', index=False)
    return df_final


def obtener_numeros(codigo):
   # Utilizar expresiones regulares para encontrar los números
    numeros = re.findall(r'\d+', codigo)

    # Concatenar los números y convertirlos a un solo entero
    numero_completo = ''.join(numeros)

    return int(numero_completo)


def predict(hacienda):
    df = GenerateDF(hacienda)
    print(df)
    df = df.drop(['Relat_Hum_Min'], axis=1)
    data=[]
    def procesar_fila(row):
        # Rellenar el arreglo de objetos data con la información necesaria
        obj = {
            'Id_Lote': row['Id_Lote'],
            'edad': row['edad'],
            'E1': row['E1'],
            'E2': row['E2'],
            'E3': row['E3'],
            'E4': row['E4'],
            'E5': row['E5'],
            'grade_monilla': row['grade_monilla'],
            'Evapotranspiration_Crop': row['Evapotranspiration_Crop'],
            'qq': row['qq'],
            'Nvdi': row['Nvdi'],
            'Relat_Hum_Max_Temp': row['Relat_Hum_Max_Temp'],
            'Temp_Air_Max': row['Temp_Air_Max'],
            'Temp_Air_Min': row['Temp_Air_Min'],
            'Dew_Temp_Max': row['Dew_Temp_Max'],
            'Precipitacion': row['Precipitacion'],
            'Sunshine_Duration': row['Sunshine_Duration'],
            'date': pd.to_datetime(str(row['date'])),
        }
        data.append(obj)

    # Aplicar la función procesar_fila a lo largo de las filas del DataFrame
    df.apply(procesar_fila, axis=1)
    # print(df['date'].dt.year)
    # df['anio']=df['date']
    #df['year'] = df['date'].dt.year.astype(int)
    #df['date'] = df['date'].dt.month.astype(int)
    #df.rename(columns={'date': 'month'}, inplace=True)
    #df['lote'] = df['lote'].apply(obtener_numeros)
   ## df['year'] = df['date'].dt.year
    #df.to_excel('dataset_Monilla.xlsx', index=False)
    #df.to_csv('dataset_Monilla.csv', index=False)
    return data
