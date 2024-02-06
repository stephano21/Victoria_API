from django.db.models import Avg, Sum,Count
from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote, Proyecto, Produccion,Hacienda
import pandas as pd
import re  # Expreciones regulares
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta,date
from pandas.tseries.offsets import MonthEnd
from django.shortcuts import get_object_or_404

def GertTreeByLot():
    queryset = Proyecto.objects.select_related('Id_Hacienda').filter(
        Activo=True, 
        Id_Hacienda_id=1, 
        ).annotate(Plantas=Count('lote__planta'))  
    data = [
        {
            'Victoria': obj.Nombre,
            'Plantas': obj.Plantas,
            #f'{column_name}': getattr(obj, column_name),
        }
        for obj in queryset
    ]
    print(data)  
    return data

def GetLecturasPerMonth(From, to):
    # Obtener el objeto de la Hacienda (puedes personalizar esto según tu modelo)
    hacienda = get_object_or_404(Hacienda, id=1)

    queryset = Proyecto.objects.select_related('Id_Hacienda').filter(
        Activo=True, 
        Id_Hacienda=hacienda,
    )

    def parse_fecha(fecha):
        if isinstance(fecha, str):
            return datetime.strptime(fecha, '%Y-%m-%d')
        return None

    # Convertir las fechas
    if From and to:
        From = parse_fecha(From)
        to = parse_fecha(to)
        queryset = queryset.filter(lote__planta__lectura__FechaVisita__range=(From, to))

    # Si solo se proporciona la fecha de inicio, filtrar por fechas mayores o iguales a la fecha de inicio
    elif From:
        From = parse_fecha(From)
        queryset = queryset.filter(lote__planta__lectura__FechaVisita__gte=From)

    # Si solo se proporciona la fecha de fin, filtrar por fechas menores o iguales a la fecha de fin
    elif to:
        to = parse_fecha(to)
        queryset = queryset.filter(lote__planta__lectura__FechaVisita__lte=to)

    # Calcular el promedio de los campos E1, E2, E3, E4, E5
    promedio = queryset.aggregate(
        E1_avg=Avg('lote__planta__lectura__E1'),
        E2_avg=Avg('lote__planta__lectura__E2'),
        E3_avg=Avg('lote__planta__lectura__E3'),
        E4_avg=Avg('lote__planta__lectura__E4'),
        E5_avg=Avg('lote__planta__lectura__E5'),
    )

    data = {
        'E1': promedio['E1_avg'],
        'E2': promedio['E2_avg'],
        'E3': promedio['E3_avg'],
        'E4': promedio['E4_avg'],
        'E5': promedio['E5_avg'],
    }

    print(data)  
    return data