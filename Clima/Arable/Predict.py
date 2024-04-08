from django.db.models import Avg, Sum, Q
from Clima.models import Daily_Indicadores
from Predict.models import DatasetPred, DatasetTrain
from Predict.serializers import DatasetTrainSerializer, DatasetPredSerializer
from Hacienda.models import Lectura, Produccion
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
from joblib import load

from utils.Console import console


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


def get_column_valuev2(df, date, column_name, months_ago, lotestr, hacienda):
    # Convertir la fecha hace "months_ago" meses a datetime
    # target_date = pd.to_datetime(date - relativedelta(months=months_ago))
    # Obtener la fecha hace "months_ago" meses
    console.log(f"{date}, {lotestr} meses a tras {months_ago} Estadio {column_name}")
    target_date = date.to_timestamp() - pd.DateOffset(months=months_ago)
    # Obtener el último día del mes de target_date
    last_day_of_month = target_date + pd.offsets.MonthEnd(0)
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True,
        Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda,
        Id_Planta__Id_Lote__Codigo_Lote=lotestr,
        FechaVisita__gte=target_date,
        FechaVisita__lte=last_day_of_month,)
    data = [
        {
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote,
            f'{column_name}': getattr(obj, column_name),
        }
        for obj in queryset
    ]
    dfRetorno = pd.DataFrame(data)
    # Obtener el valor de la columna deseada
    if len(dfRetorno) > 0:
        dfRetorno = dfRetorno.groupby([dfRetorno['lote']])[
            [column_name]].sum().reset_index()
        return int(dfRetorno[column_name].iloc[0])
    else:
        return 0


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
            'Evapotranspiration_Crop': 0,
            'Nvdi': 0,
            'Relat_Hum_Max_Temp': 0,
            'Temp_Air_Max': 0,
            'Temp_Air_Min': 0,
            'Dew_Temp_Max': 0,
            'Precipitacion': 0,
            'Sunshine_Duration': 0,
        }
    return {
        'Evapotranspiration_Crop': queryset.aggregate(sum_evapotranspiration_crop=Sum('Evapotranspiration_Crop'))['sum_evapotranspiration_crop'],
        'Nvdi': queryset.aggregate(sum_nvdi=Sum('Nvdi'))['sum_nvdi'],
        'Relat_Hum_Max_Temp': queryset.aggregate(avg_relat_hum_max_temp=Avg('Relat_Hum_Max_Temp'))['avg_relat_hum_max_temp'],
        'Temp_Air_Max': queryset.aggregate(max_temp_air_max=Avg('Temp_Air_Max'))['max_temp_air_max'],
        'Temp_Air_Min': queryset.aggregate(min_temp_air_min=Avg('Temp_Air_Min'))['min_temp_air_min'],
        'Dew_Temp_Max': queryset.aggregate(max_dew_temp_max=Avg('Dew_Temp_Max'))['max_dew_temp_max'],
        'Precipitacion': queryset.aggregate(sum_precipitacion=Sum('Precipitacion'))['sum_precipitacion'],
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
            'Plantas': obj.Id_Lote.Num_Plantas,
            'Id_Lote': obj.Id_Lote.id,
            'hectareas': obj.Id_Lote.Hectareas,
        }
        for obj in queryset
    ]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'], df['edad'], df['Plantas'], df['Id_Lote'], df['hectareas']])[
        'qq'].sum().reset_index()
    df.to_excel("ProduccionDF.xlsx", index=False)
    return df


def calculate_age(fecha_siembra):
    hoy = datetime.now()
    edad = hoy.year - fecha_siembra.year - \
        ((hoy.month, hoy.day) < (fecha_siembra.month, fecha_siembra.day))
    return edad


def filter_by_date_range(queryset, start_date=None, end_date=None):
    if start_date and end_date:
        queryset = queryset.filter( FechaVisita__year__gte=start_date.year,
                                FechaVisita__year__lte=end_date.year,
                                FechaVisita__month__gte=start_date.month,
                                FechaVisita__month__lte=end_date.month)
    elif start_date:
        queryset = queryset.filter(FechaVisita__year=start_date.year,
                                FechaVisita__month=start_date.month)
    elif end_date:
        queryset = queryset.filter(FechaVisita__year=end_date.year,
                                FechaVisita__month=end_date.month)
    return queryset

def filter_by_date_rangeW(queryset, start_date=None, end_date=None):
    if start_date and end_date:
        queryset = queryset.filter(Date__year__gte=start_date.year,
                                Date__year__lte=end_date.year,
                                Date__month__gte=start_date.month,
                                Date__month__lte=end_date.month)
    elif start_date:
        queryset = queryset.filter(Date__year=start_date.year,
                                Date__month=start_date.month)
    elif end_date:
        queryset = queryset.filter(Date__year=end_date.year,
                                Date__month=end_date.month)
    return queryset


def GetLecturasv1(hacienda,start_date = None,end_date = None):
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Activo=True, Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=hacienda)
    queryset = filter_by_date_range(queryset, start_date, end_date)
    data = []
    for obj in queryset:
        lectura_data = {
            'date': obj.FechaVisita,
            'hectareas': obj.Id_Planta.Id_Lote.Hectareas,
            'Plantas': obj.Id_Planta.Id_Lote.Num_Plantas,
            'Id_Lote': obj.Id_Planta.Id_Lote.id,
            'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'FechaSiembra': obj.Id_Planta.Id_Lote.FechaSiembra,
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
    # df['Plantas'] = df['Plantas'].astype(int)
    df['FechaSiembra'] = pd.to_datetime(df['FechaSiembra'])
    df['edad'] = df['FechaSiembra'].apply(calculate_age)
    # print(df)
    # Calcular las columnas E1, E2, E3 de hace 3, 2, 1 meses respectivamente
    df = df.groupby([df['date'].dt.to_period("M"), df['lote'], df['Id_Lote'], df['edad'], df['Plantas'], df['hectareas']])[
        ['E1', 'E2', 'E3', 'E4', 'E5', 'GR1', 'GR2', 'GR3', 'GR4', 'GR5', 'Cherelles']].mean().reset_index()
    # Seleccionar solo las columnas objetivo
    target_columns = df.loc[:, 'GR1':'GR5']
    Losttarget_columns = df.loc[:, 'GR2':'GR5']
    # Obtener la columna con el mayor valor en cada fila en el rango específico
    max_column = target_columns.idxmax(axis=1)
    # Asignar un número según la posición de la columna
    df['grade_monilla'] = max_column.str.extract('(\d+)')
    df['perdida'] = Losttarget_columns.mean(axis=1)
    df = df.drop(['GR1', 'GR2', 'GR3', 'GR4', 'GR5'], axis=1)
    df['Plantas'] = df['Plantas'].astype(int)
    return df


def GetWeather(start_date = None,end_date = None):
    queryset = Daily_Indicadores.objects.all()
    queryset = filter_by_date_rangeW(queryset, start_date, end_date)
    data = [{'date': obj.Date,
            # 'temp': obj.Temp_Air_Mean,
            # 'Evapotranspiration': obj.Evapotranspiration,
            'Evapotranspiration_Crop': obj.Evapotranspiration_Crop,
            'Nvdi': obj.Ndvi,
            # 'Relat_Hum_Min': obj.Relat_Hum_Min,
            'Relat_Hum_Max_Temp': obj.Relat_Hum_Max_Temp,
            # 'Relat_Hum_Min_Temp': obj.Relat_Hum_Min_Temp,
            'Temp_Air_Max': obj.Temp_Air_Max,
            'Temp_Air_Min': obj.Temp_Air_Min,
            'Dew_Temp_Max': obj.Dew_Temp_Max,
            'Precipitacion': obj.Precipitacion,
            # 'Precipitacion_Hours': obj.Precipitacion_Hours,
            # 'Sea_Level_Pressure': obj.Sea_Level_Pressure,
            # 'Vapor_Pressure_Deficit': obj.Vapor_Pressure_Deficit,
            # 'Dew_Temp_Mean': obj.Dew_Temp_Mean,
            # 'Crop_Water_Demand': obj.Crop_Water_Demand,
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
    df = df.groupby(df['date'].dt.to_period("M")).agg({  # 'temp': 'mean',
        # 'Evapotranspiration': 'sum',
        'Evapotranspiration_Crop': 'sum',
        'Nvdi': 'sum',
        # 'Relat_Hum_Min': 'mean',
        'Relat_Hum_Max_Temp': 'mean',
        'Temp_Air_Max': 'mean',
        'Temp_Air_Min': 'mean',
        'Dew_Temp_Max': 'mean',
        'Precipitacion': 'sum',
        # 'Precipitacion_Hours': 'sum',
        # 'Sea_Level_Pressure': 'mean',
        # 'Vapor_Pressure_Deficit': 'mean',
        # 'Dew_Temp_Mean': 'mean',
        # 'Crop_Water_Demand': 'sum',
        'Sunshine_Duration': 'sum'}).reset_index()
    df.to_dict(orient='records')
    df.to_excel("DatosClimaticos.xlsx", index=False)
    return df


def GenerateDF(hacienda, train=False):
    dfLecturas = GetLecturasv1(hacienda)
    dfWeather = GetWeather()
    if train:
        dfProduction = getProduction(hacienda)
        df_merged = pd.merge(dfLecturas, dfProduction, on=[
            'date', 'lote', 'edad', 'Plantas', 'Id_Lote', 'hectareas'], how='right')
        df_merged = df_merged.fillna(0)
    # Hacer merge con dfWeather usando 'date'
        df_final = pd.merge(df_merged, dfWeather, on='date', how='inner')
    else:
        df_final = pd.merge(dfLecturas, dfWeather, on='date', how='inner')
        df_final = df_final.fillna(0)
    for i in range(3, 0, -1):
        df_final[f'E{4-i}'] = df_final.apply(
            lambda row: get_column_valuev2(df_final, row['date'], f'E{4-i}', i, row['lote'], hacienda), axis=1)
    columnas_float = ['E1', 'E2', 'E3', 'E4', 'E5', 'Plantas', 'hectareas']
    # Convertir las columnas a tipo float
    df_final[columnas_float] = df_final[columnas_float].astype(float)
    # Lista de prefijos para las nuevas columnas de totales
    totales_prefijos = ['Total_E1', 'Total_E2', 'Total_E3',
                        'Total_E4', 'Total_E5']  # retiro 60 pago 40 de la tarjeta
    # Bucle para calcular los totales
    for i, prefijo in enumerate(totales_prefijos, start=1):
        df_final[prefijo] = (
            ((df_final[f'E{i}']/12) * df_final['Plantas']) / df_final['hectareas'])/100
    df_final['lost'] = ((((df_final['perdida'] + df_final['Cherelles'])/12)
                        * df_final['Plantas'] / df_final['hectareas']))/100
    df_final = df_final.fillna(0)
    df_final.to_excel('probandtetssdhj.xlsx', index=False)
    print(df_final)
    return df_final, train


def obtener_numeros(codigo):
    # Utilizar expresiones regulares para encontrar los números
    numeros = re.findall(r'\d+', codigo)
    # Concatenar los números y convertirlos a un solo entero
    numero_completo = ''.join(numeros)
    return int(numero_completo)

# TODO: Generar df sin produccion y filtrar por hacienda



def ExisteDataset(hacienda, date):
    return DatasetPred.objects.filter(
        Id_Lote__Id_Proyecto__Id_Hacienda=hacienda, date__month=date.month, date__year=date.year).exists()


def get_latest_date():
    latest_date = DatasetPred.objects.order_by('-date').first()
    if latest_date:
        return latest_date.date
    else:
        return None


def GetDataSetPred(date):
    fecha_5_meses_atras = date - timedelta(days=30*5)

# Filtra los datos usando el rango de fechas
    queryset = DatasetPred.objects.filter(date__range=(fecha_5_meses_atras, date))
    # queryset = Dataset.objects.filter(Q(date__gte=date))
    data = []
    for obj in queryset:
        dataset = {
            'Id_Lote': obj.Id_Lote.id,
            'date': obj.date,
            'Total_E1': obj.Total_E1,
            'Total_E2': obj.Total_E2,
            'Total_E3': obj.Total_E3,
            'Total_E4': obj.Total_E4,
            'Total_E5': obj.Total_E5,
            'Evapotranspiration_Crop': obj.Evapotranspiration_Crop,
            'Nvdi': obj.Nvdi,
            'Relat_Hum_Max_Temp': obj.Relat_Hum_Max_Temp,
            'Temp_Air_Max': obj.Temp_Air_Max,
            'Temp_Air_Min': obj.Temp_Air_Min,
            'Dew_Temp_Max': obj.Dew_Temp_Max,
            'Precipitacion': obj.Precipitacion,
            'Sunshine_Duration': obj.Sunshine_Duration,
            'edad': obj.edad,
            'grade_monilla': obj.grade_monilla,
            'lost': obj.lost,
        }
        data.append(dataset)
    df = pd.DataFrame(data)
    return df


def SaveDataSetTrain(df):
    console.log("Guardando dataset to train")
    df['date'] = df['date'].astype(str)
    df['date'] = df['date'] + '-01'
    console.log(df)
    
    columns_to_round = ['Total_E1', 'Total_E2',
                        'Total_E3', 'Total_E4', 
                        'Total_E5', 'lost','Temp_Air_Min', 
                        'Dew_Temp_Max','Precipitacion', 
                        'Sunshine_Duration', 'Evapotranspiration_Crop', 
                        'Nvdi', 'Relat_Hum_Max_Temp','Temp_Air_Max']
    # Aplica la función round a las columnas seleccionadas
    df[columns_to_round] = df[columns_to_round].astype(float)
    df[columns_to_round] = df[columns_to_round].round(decimals=13)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    print(df)
    data = []
    for index, row in df.iterrows():
        obj = {}
        for column in df.columns:
            # Create a new object
            # Set the property name as the column name and the value as the corresponding cell value
            obj[column] = row[column]
            # Add the object to the data array
        data.append(obj)
    serializer = DatasetTrainSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    df = df.drop(['E1', 'E2', 'E3', 'E4', 'E5', 'Plantas', 'hectareas',
                'lote', 'Id_Lote', 'Cherelles', 'perdida'], axis=1)
    return data


def SaveDataSetPred(df):
    console.log("Guardando dataset to train")
    df['date'] = df['date'].astype(str)
    df['date'] = df['date'] + '-01'
    console.log(df)
    
    columns_to_round = ['Total_E1', 'Total_E2',
                        'Total_E3', 'Total_E4', 
                        'Total_E5', 'lost','Temp_Air_Min', 
                        'Dew_Temp_Max','Precipitacion', 
                        'Sunshine_Duration', 'Evapotranspiration_Crop', 
                        'Nvdi', 'Relat_Hum_Max_Temp','Temp_Air_Max']
    # Aplica la función round a las columnas seleccionadas
    df[columns_to_round] = df[columns_to_round].astype(float)
    df[columns_to_round] = df[columns_to_round].round(decimals=13)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    print(df)
    data = []
    for index, row in df.iterrows():
        obj = {}
        for column in df.columns:
            # Create a new object
            # Set the property name as the column name and the value as the corresponding cell value
            obj[column] = row[column]
            # Add the object to the data array
        data.append(obj)
    serializer = DatasetPredSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    df = df.drop(['E1', 'E2', 'E3', 'E4', 'E5', 'Plantas', 'hectareas',
                'lote', 'Id_Lote', 'Cherelles', 'perdida'], axis=1)
    return data