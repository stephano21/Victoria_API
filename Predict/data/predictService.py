#TODO: Generar df sin produccion y filtrar por hacienda
from joblib import load
from Clima.Arable.Predict import ExisteDataset, GenerateDF, GetDataSet, SaveDataSet, get_latest_date
from utils.Console import console
import os
import pandas as pd
def predict(hacienda, date):
    df = None
    current_directory = os.getcwd()
    dir = os.path.join(current_directory, "Predict", "data", "Modelo.joblib")
    console.warn(f"Directorio actual:{get_latest_date()}")
    if not ExisteDataset(hacienda, date) and not get_latest_date():
        console.warn("Coonstruyendo Historico  desde 0")
        df = GenerateDF(hacienda)
        SaveDataSet(df)
    elif not ExisteDataset(hacienda, date) and get_latest_date():
        console.log("Get By Date")
        df =  GetDataSet(get_latest_date())
        console.log(df)

    if df is not None:
        console.log("Predicting....")
        # Cargar el modelo desde el archivo
        #if 2==2: return "Ok"
        loaded_model = load(dir, 'r')
        console.log(df)
        df['date'] = df['date'].dt.tz_localize(None)
        df.to_excel("df.xlsx")
        #df = df.drop(columns=['date','Id_Lote'])
        #df = df.astype(float)
        predictions_prod = loaded_model.predict(df.drop(columns=['date','Id_Lote']).astype(float))
        dfPred = pd.DataFrame(predictions_prod, columns=['Predictions'])
        console.log(dfPred)
        return predictions_prod
