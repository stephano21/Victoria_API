# TODO: Generar df sin produccion y filtrar por hacienda
from datetime import datetime
from typing import List, Dict
import uuid
import calendar
from joblib import load
from Clima.Arable.Predict import (
    ExisteDataset,
    GenerateDF,
    GetDataSetPred,
    SaveDataSetPred,
    SaveDataSetTrain,
    get_latest_date,
)
from Hacienda.models import Lectura
from Predict.models import HistorialPredict
from Predict.serializers import HistorialPredictSerializer
from utils.Console import console
import os
import pandas as pd
from django.db.models import Q, Max


def SaveHistorialPredict(df: pd.DataFrame, user:str="System"):
    groupPrediction = str(uuid.uuid4())
    console.log(groupPrediction)
    # Ordenar el DataFrame por la columna de fecha en orden descendente
    df_sorted = df.sort_values(by="date", ascending=False)
    # Obtener el rango de valores únicos basados en la columna de fecha
    unique_dates = df_sorted["date"].unique()
    # Crear un diccionario que mapee cada fecha única a su posición en la lista ordenada
    date_position = {date: i + 1 for i, date in enumerate(unique_dates)}
    # Asignar los valores del rango en función de la posición de la fecha en la lista ordenada
    df_sorted["Orden"] = df_sorted["date"].map(date_position)
    df_sorted["Predictions"] = df_sorted["Predictions"].astype(float)

    df_sorted["Predictions"] = df_sorted["Predictions"].round(decimals=5)
    for index, row in df_sorted.iterrows():
        fecha = row["date"].to_pydatetime().date()
        serializer_data = {
            "Id_Lote": row["Id_Lote"],
            "GroupPrediction": groupPrediction,
            "Qq": row["Predictions"],
            "Fecha": fecha,
            "Usuario": user,
            "Orden": row["Orden"],
        }
        serializer = HistorialPredictSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            console.log("Historial registrado con exito!")
        else:
            console.error("No se pudo guardar el historial")
            console.error(serializer.errors)


def predict(hacienda:int, date:datetime, username:str="System"):
    console.log("Predicting....")
    df = None
    current_directory = os.getcwd()
    dir = os.path.join(current_directory, "Predict", "data", "Modelo.joblib")
    console.warn(f"Directorio actual:{dir}")
    if not ExisteDataset(hacienda, date) and not get_latest_date():
        console.warn("Coonstruyendo Historico  desde 0")
        df, train = GenerateDF(hacienda)
        if not train:
            SaveDataSetPred(df)
        df = GetDataSetPred(get_latest_date())
        SaveHistorialPredict(df, username)
    elif not ExisteDataset(hacienda, date) and get_latest_date():
        console.log("Get By Date")
        df = GetDataSetPred(get_latest_date())
        console.log(df)

    if df is not None:
        loaded_model = load(dir, "r")
        df["date"] = df["date"].dt.tz_localize(None)
        IdsLotes = pd.DataFrame(df, columns=["Id_Lote", "date"])
        # df = df.astype(float)
        predictions_prod = loaded_model.predict(
            df.drop(columns=["date", "Id_Lote"]).astype(float)
        )
        dfPred = pd.DataFrame(predictions_prod, columns=["Predictions"])
        # df_concatenado = pd.concat([IdsLotes, dfPred])
        IdsLotes = IdsLotes.join(dfPred["Predictions"])
        save = SaveHistorialPredict(IdsLotes, username)
        return predictions_prod


def month_as_string(month):
    if month < 1 or month > 12:
        return "Número de mes inválido"

    # Diccionario de nombres de meses en español
    nombres_meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    # Obtener el nombre del mes correspondiente al número proporcionado
    nombre_mes = nombres_meses[month]
    return nombre_mes


def get_latest_groupPrediction():
    return HistorialPredict.objects.order_by("-FechaRegistro").first().GroupPrediction

def get_last_date_lectura(hacienda: int):
    queryset = Lectura.objects.select_related('Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda').filter(
        Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda=hacienda, Activo=True
    ).order_by("-FechaVisita")
    if queryset.exists():
        return queryset.first().FechaVisita
    return None

def get_predict(hacienda: int, date: datetime,group):
    # Obtener todos los registros dentro del rango de fecha dado
    #group = get_latest_groupPrediction()
    queryset = HistorialPredict.objects.filter(
        GroupPrediction=group, Activo=True
    ).order_by("Orden")

    data = [
        {
            "Id": item.GroupPrediction,
            "Project": item.Id_Lote.Id_Proyecto.Nombre,
            "Hectareas": item.Id_Lote.Hectareas,
            "qq/ha": item.Qq,
            "Orden": item.Orden,
        }
        for item in queryset
    ]
    df = pd.DataFrame(data)
    data_agrupada = (
        df.groupby(["Project", "Orden"])[["qq/ha", "Hectareas"]].sum().reset_index()
    )
    data_agrupada = data_agrupada.sort_values(by="Orden")
    data_agrupada["Mes"] = data_agrupada["Orden"].apply(
        lambda x: month_as_string(date.month if x == 1 else date.month + x)
    )
    data_agrupada["Pred"] = data_agrupada["qq/ha"] * data_agrupada["Hectareas"]

    resultado: List[Dict[str, List[Dict[str, float]]]] = []

    # Obtener los meses presentes en el conjunto de datos
    meses_presentes = data_agrupada["Mes"].unique()

    # Iterar sobre cada mes presente
    for mes in meses_presentes:
        proyectos_mes: List[Dict[str, float]] = []

        # Filtrar los datos solo para el mes actual
        datos_mes = data_agrupada[data_agrupada["Mes"] == mes]

        # Iterar sobre cada fila de datos para el mes actual
        for _, row in datos_mes.iterrows():
            proyecto_info = {
                "Project": row["Project"],
                "Pred": row["Pred"],
                "qq/has": row["qq/ha"],
            }
            proyectos_mes.append(proyecto_info)

        # Agregar los proyectos del mes al resultado
        resultado.append({"mes": mes, "data": proyectos_mes})

    return resultado

def get_all_predict(hacienda: int, date: datetime):
    queryset = HistorialPredict.objects.filter(Activo=True).order_by("Orden")
    data = [
        {
            "Id": item.GroupPrediction,
            "Project": item.Id_Lote.Id_Proyecto.Nombre,
            "Hectareas": item.Id_Lote.Hectareas,
            "qq/ha": item.Qq,
            "Orden": item.Orden,
        }
        for item in queryset
    ]
    df = pd.DataFrame(data)
    data_agrupada = (
        df.groupby(["Project", "Orden"])[["qq/ha", "Hectareas"]].sum().reset_index()
    )
    data_agrupada = data_agrupada.sort_values(by="Orden")
    data_agrupada["Mes"] = data_agrupada["Orden"].apply(
        lambda x: month_as_string(date.month if x == 1 else date.month + x)
    )
    data_agrupada["Pred"] = data_agrupada["qq/ha"] * data_agrupada["Hectareas"]

    resultado: List[Dict[str, List[Dict[str, float]]]] = []

    # Obtener los meses presentes en el conjunto de datos
    meses_presentes = data_agrupada["Mes"].unique()

    # Iterar sobre cada mes presente
    for mes in meses_presentes:
        proyectos_mes: List[Dict[str, float]] = []

        # Filtrar los datos solo para el mes actual
        datos_mes = data_agrupada[data_agrupada["Mes"] == mes]

        # Iterar sobre cada fila de datos para el mes actual
        for _, row in datos_mes.iterrows():
            proyecto_info = {
                "Project": row["Project"],
                "Pred": row["Pred"],
                "qq/has": row["qq/ha"],
            }
            proyectos_mes.append(proyecto_info)

        # Agregar los proyectos del mes al resultado
        resultado.append({"mes": mes, "data": proyectos_mes})

    return resultado
def update_dataset_pred(hacienda: int):
    try:
        
        latest_date = get_latest_date()
        console.log(f"Fecha más reciente data set: {latest_date}")

        # Obtener la fecha más reciente en la que se realizó una lectura
        latest_date_lectura = get_last_date_lectura(hacienda)
        console.log(f"Fecha más reciente de lectura: {latest_date_lectura}")

        # Si no hay una fecha más reciente de lectura, no se puede actualizar el dataset
        if not latest_date_lectura:
            console.error("No hay una fecha de lectura reciente")
            return "No hay una fecha de lectura reciente"

        # Si la fecha más reciente de lectura es mayor a la fecha más reciente del dataset
        if latest_date:
            if latest_date_lectura > latest_date:
                console.warn("Actualizando el dataset by range...")
                # Obtener el dataset más reciente
                dataset, train = GenerateDF(hacienda,False, latest_date, latest_date_lectura)
                if not train:
                    SaveDataSetPred(dataset)
                    return "Dataset actualizado con éxito"
            else:
                console.log("No es necesario actualizar el dataset")
                return "No es necesario actualizar el dataset"

        else:
            console.warn("Creando data set...")
            # Obtener el dataset más reciente
            dataset, train = GenerateDF(hacienda,False, None, latest_date_lectura)
            if not train:
                SaveDataSetPred(dataset)
                return "Dataset actualizado con éxito"
    except Exception as e:
        raise e