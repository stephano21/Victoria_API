from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote,Proyecto, Produccion
import pandas as pd
#Sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, accuracy_score, median_absolute_error,r2_score
def GetLecturas():
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(Activo=True, Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=1)

    data = [
        {
            'date': obj.FechaVisita,
            #'producion_real': obj.Id_Planta.Id_Lote.Id_Proyecto.Codigo_Proyecto if obj.Id_Planta and obj.Id_Planta.Id_Lote and  obj.Id_Planta.Id_Lote.Id_Proyecto else None,
            #'lote': obj.Id_Planta.Id_Lote.Codigo_Lote if obj.Id_Planta and obj.Id_Planta.Id_Lote else None,
            'planta': obj.Id_Planta.Codigo_Planta,
            #'hectareas': obj.Id_Planta.Id_Lote.Hectareas,
            #'densidad': obj.Id_Planta.Id_Lote.Id_Proyecto.Densidad,
            'E1': obj.E1,
            'E2': obj.E2,
            'E3': obj.E3,
            'E4': obj.E4,
            'E5': obj.E5
        } 
        for obj in queryset
    ]
    df = pd.DataFrame(data)
    df['date']= df['date'].dt.to_period("M")
    # Convertir los datos a DataFrame de pandas
    return df

def getProduction():
    queryset = Produccion.objects.select_related('Id_Proyecto__Id_Hacienda').filter(Activo=True, Id_Proyecto__Id_Hacienda_id=1)

    data = [
        {
            'date': obj.Fecha,
            'qq': obj.Qq,
            'hacienda': obj.Id_Proyecto.Id_Hacienda.codigo,
        }
        for obj in queryset
    ]
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby([df['date'].dt.to_period("M"), df['hacienda']])['qq'].sum().reset_index()

def GetWeather():
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
    df = df.groupby(df['date'].dt.to_period("M")).agg({'temp': 'mean',
                                                        'Evapotranspiration': 'sum',
                                                        'Evapotranspiration_Crop': 'sum',
                                                        'Nvdi': 'sum',
                                                        'Relat_Hum_Min': 'mean',
                                                        'Relat_Hum_Max_Temp': 'mean',
                                                        'Temp_Air_Max': 'max',
                                                        'Temp_Air_Min': 'min',
                                                        'Dew_Temp_Max': 'max',
                                                        'Precipitacion': 'sum',
                                                        'Precipitacion_Hours': 'sum',
                                                        'Sea_Level_Pressure': 'mean',
                                                        'Vapor_Pressure_Deficit': 'mean',
                                                        'Dew_Temp_Mean': 'mean',
                                                        'Crop_Water_Demand': 'sum',
                                                        'Sunshine_Duration': 'sum'}).reset_index()

    df.to_dict(orient='records') 
    return df


def GenerateDF():
    dfLecutas = GetLecturas()
    dfProduction = getProduction()
    dfWeather = GetWeather()
    df = pd.merge(dfLecutas, dfProduction, on='date',how='inner' ).merge(dfWeather, on='date',how='inner' )
    #df.to_csv('Clima.csv', index=False)
    #df.to_excel('DFNew.xlsx', index=False)
    return df
def predict():
    df = GenerateDF()
    df = df.drop(['planta','hacienda','Relat_Hum_Min'],axis=1)
    df['date'] = df['date'].dt.month


    # Elimina la columna de fechas y la columna objetivo 'qq' para el conjunto X y 'qq' para y
    X = df.drop(['qq'], axis=1)
    y = df['qq']

    # Manejo de datos faltantes (rellenar con la media en este ejemplo)
    #X.fillna(X.mean(), inplace=True)

    # Codificación de variables categóricas (si es necesario)
    #X = pd.get_dummies(X)

    # Escalado de características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # División de datos
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    # Crear un DataFrame para almacenar las métricas
    metrics_df = pd.DataFrame(columns=['Model', 'Metric', 'Value'])

    # SVM Regresión
    svm_regressor = SVR()
    svm_regressor.fit(X_train, y_train)
    svm_predictions = svm_regressor.predict(X_test)
    svm_mse = mean_squared_error(y_test, svm_predictions)
    svm_r2 = r2_score(y_test, svm_predictions)
    mae = mean_absolute_error(y_test, svm_predictions)
    rmse = mean_squared_error(y_test, svm_predictions, squared=False)
    explained_variance = explained_variance_score(y_test, svm_predictions)
    medae = median_absolute_error(y_test, svm_predictions)

    # Almacenar métricas en el DataFrame
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'Median Absolute Error', 'Value': [medae]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'Explained Variance', 'Value': [explained_variance]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'Root Mean Squared Error', 'Value': [rmse]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'Mean Absolute Error', 'Value': [mae]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'Mean Squared Error', 'Value': [svm_mse]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'SVM Regressor', 'Metric': 'R²', 'Value': [svm_r2]})], ignore_index=True)

    # Regresión Lineal Simple
    linear_regressor = LinearRegression()
    linear_regressor.fit(X_train, y_train)
    linear_predictions = linear_regressor.predict(X_test)
    linear_mse = mean_squared_error(y_test, linear_predictions)
    linear_r2 = r2_score(y_test, linear_predictions)
    mae = mean_absolute_error(y_test, linear_predictions)
    rmse = mean_squared_error(y_test, linear_predictions, squared=False)
    explained_variance = explained_variance_score(y_test, linear_predictions)
    medae = median_absolute_error(y_test, linear_predictions)

    # Almacenar métricas en el DataFrame
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'Median Absolute Error', 'Value': [medae]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'Explained Variance', 'Value': [explained_variance]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'Root Mean Squared Error', 'Value': [rmse]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'Mean Absolute Error', 'Value': [mae]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'Mean Squared Error', 'Value': [linear_mse]})], ignore_index=True)
    metrics_df = pd.concat([metrics_df, pd.DataFrame({'Model': 'Linear Regression', 'Metric': 'R²', 'Value': [linear_r2]})], ignore_index=True)

    # Exportar el DataFrame a Excel
    metrics_df.to_excel('metrics.xlsx', index=False)

