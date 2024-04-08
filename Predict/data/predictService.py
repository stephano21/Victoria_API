# TODO: Generar df sin produccion y filtrar por hacienda
import uuid
from joblib import load
from Clima.Arable.Predict import ExisteDataset, GenerateDF, GetDataSetPred, SaveDataSetPred,SaveDataSetTrain, get_latest_date
from Predict.serializers import HistorialPredictSerializer
from utils.Console import console
import os
import pandas as pd


def SaveHistorialPredict(df, user="System"):
    groupPrediction = str(uuid.uuid4())
    console.log(groupPrediction)
    # Ordenar el DataFrame por la columna de fecha en orden descendente
    df_sorted = df.sort_values(by='date', ascending=False)
    # Obtener el rango de valores únicos basados en la columna de fecha
    unique_dates = df_sorted['date'].unique()
    # Crear un diccionario que mapee cada fecha única a su posición en la lista ordenada
    date_position = {date: i + 1 for i, date in enumerate(unique_dates)}
    # Asignar los valores del rango en función de la posición de la fecha en la lista ordenada
    df_sorted['Orden'] = df_sorted['date'].map(date_position)
    df_sorted['Predictions'] = df_sorted['Predictions'].astype(float)

    df_sorted['Predictions'] = df_sorted['Predictions'].round(decimals=5)
    for index, row in df_sorted.iterrows():
        fecha = row['date'].to_pydatetime().date()
        serializer_data = {
            'Id_Lote': row['Id_Lote'],
            'GroupPrediction': groupPrediction,
            'Qq': row['Predictions'],
            'Fecha': fecha,
            'Usuario': user,
            'Orden': row['Orden']
        }
        serializer = HistorialPredictSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            console.log("Historial registrado con exito!")
        else:
            console.error("No se pudo guardar el historial")
            console.error(serializer.errors)

def predict(hacienda, date, username):
    df = None
    current_directory = os.getcwd()
    dir = os.path.join(current_directory, "Predict", "data", "Modelo.joblib")
    console.warn(f"Directorio actual:{dir}")
    if not ExisteDataset(hacienda, date) and not get_latest_date():
        console.warn("Coonstruyendo Historico  desde 0")
        df,train = GenerateDF(hacienda)
        if not train:
            SaveDataSetPred(df)
        SaveHistorialPredict(df, username)
        df = GetDataSetPred(get_latest_date())
    elif not ExisteDataset(hacienda, date) and get_latest_date():
        console.log("Get By Date")
        df = GetDataSetPred(get_latest_date())
        console.log(df)

    if df is not None:
        console.log("Predicting....")
        loaded_model = load(dir, 'r')
        console.log(df)
        df['date'] = df['date'].dt.tz_localize(None)
        df.to_excel("df.xlsx")
        IdsLotes = pd.DataFrame(df, columns=['Id_Lote', 'date'])
        console.log(IdsLotes)
        # df = df.astype(float)
        predictions_prod = loaded_model.predict(
            df.drop(columns=['date', 'Id_Lote']).astype(float))
        dfPred = pd.DataFrame(predictions_prod, columns=['Predictions'])
        # df_concatenado = pd.concat([IdsLotes, dfPred])
        IdsLotes = IdsLotes.join(dfPred['Predictions'])
        save = SaveHistorialPredict(IdsLotes, username)
        console.log(IdsLotes)
        return predictions_prod
