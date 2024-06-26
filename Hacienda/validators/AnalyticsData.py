from django.db.models import Avg, Sum, Count
from Clima.models import Daily_Indicadores
from Hacienda.models import Lectura, Planta, Lote, Proyecto, Produccion, Hacienda
import pandas as pd
import re  # Expreciones regulares
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from pandas.tseries.offsets import MonthEnd
from django.shortcuts import get_object_or_404
from Users.models import Perfil


def parse_fecha(fecha):
    if isinstance(fecha, str):
        return datetime.strptime(fecha, "%Y-%m-%d")
    return None


def OrderByVictoria(data):
    return sorted(data, key=lambda x: x["Victoria"])


def GertTreeByLot(hacienda_id):
    queryset = (
        Proyecto.objects.select_related("Id_Hacienda")
        .filter(
            Activo=True,
            Id_Hacienda_id=hacienda_id,
        )
        .annotate(Plantas=Count("lote__planta"))
    )
    data = [
        {
            "Victoria": obj.Nombre,
            "Plantas": obj.Plantas,
            # f'{column_name}': getattr(obj, column_name),
        }
        for obj in queryset
    ]
    data = OrderByVictoria(data)
    return data


def GetProductionByVictoria(From, to, hacienda_id):
    queryset = Proyecto.objects.select_related("Id_Hacienda").filter(
        Activo=True,
        Id_Hacienda=hacienda_id,
    )
    # Convertir las fechas
    if From and to:
        From = parse_fecha(From)
        to = parse_fecha(to)
        queryset = queryset.filter(lote__produccion__Fecha__range=(From, to))

    # Si solo se proporciona la fecha de inicio, filtrar por fechas mayores o iguales a la fecha de inicio
    elif From:
        From = parse_fecha(From)
        queryset = queryset.filter(lote__produccion__Fecha__gte=From)

    # Si solo se proporciona la fecha de fin, filtrar por fechas menores o iguales a la fecha de fin
    elif to:
        to = parse_fecha(to)
        queryset = queryset.filter(lote__produccion__Fecha__lte=to)
    SumaQQ = queryset.annotate(
        qqSum=Sum("lote__produccion__Qq"),
    ).values("Nombre", "qqSum")
    data = [
        {
            "Victoria": qq["Nombre"],
            "qq": round(qq["qqSum"], 2) if qq["qqSum"] else 0,
        }
        for qq in SumaQQ
    ]
    data = OrderByVictoria(data)
    return data


def GetLecturasPerMonth(From, to, hacienda_id):
    # Obtener el objeto de la Hacienda (puedes personalizar esto según tu modelo)
    queryset = Proyecto.objects.select_related("Id_Hacienda").filter(
        Activo=True,
        Id_Hacienda=hacienda_id,
    )

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
    promedios = queryset.annotate(
        E1_avg=Avg("lote__planta__lectura__E1"),
        E2_avg=Avg("lote__planta__lectura__E2"),
        E3_avg=Avg("lote__planta__lectura__E3"),
        E4_avg=Avg("lote__planta__lectura__E4"),
        E5_avg=Avg("lote__planta__lectura__E5"),
    ).values("Nombre", "E1_avg", "E2_avg", "E3_avg", "E4_avg", "E5_avg")

    # Crear una lista de diccionarios similar al formato de GertTreeByLot
    data = [
        {
            "Victoria": promedio["Nombre"],
            "E1": round(promedio["E1_avg"], 2) if promedio["E1_avg"] else 0,
            "E2": round(promedio["E2_avg"], 2) if promedio["E2_avg"] else 0,
            "E3": round(promedio["E3_avg"], 2) if promedio["E3_avg"] else 0,
            "E4": round(promedio["E4_avg"], 2) if promedio["E4_avg"] else 0,
            "E5": round(promedio["E5_avg"], 2) if promedio["E5_avg"] else 0,
        }
        for promedio in promedios
    ]
    data = OrderByVictoria(data)
    return data


def GetDiseasesPerMonth(From, to, hacienda_id):
    # Obtener el objeto de la Hacienda (puedes personalizar esto según tu modelo)
    queryset = Proyecto.objects.select_related("Id_Hacienda").filter(
        Activo=True,
        Id_Hacienda=hacienda_id,
    )

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
    promedios = queryset.annotate(
        GR1_avg=Avg("lote__planta__lectura__GR1"),
        GR2_avg=Avg("lote__planta__lectura__GR2"),
        GR3_avg=Avg("lote__planta__lectura__GR3"),
        GR4_avg=Avg("lote__planta__lectura__GR4"),
        GR5_avg=Avg("lote__planta__lectura__GR5"),
        Cherelles_avg=Avg("lote__planta__lectura__Cherelles"),
    ).values("Nombre", "GR1_avg", "GR2_avg", "GR3_avg", "GR4_avg", "GR5_avg","Cherelles_avg")

    # Crear una lista de diccionarios similar al formato de GertTreeByLot
    data = [
        {
            "Victoria": promedio["Nombre"],
            "GR1": round(promedio["GR1_avg"], 2) if promedio["GR1_avg"] else 0,
            "GR2": round(promedio["GR2_avg"], 2) if promedio["GR2_avg"] else 0,
            "GR3": round(promedio["GR3_avg"], 2) if promedio["GR3_avg"] else 0,
            "GR4": round(promedio["GR4_avg"], 2) if promedio["GR4_avg"] else 0,
            "GR5": round(promedio["GR5_avg"], 2) if promedio["GR5_avg"] else 0,
            "Cherelles": (
                round(promedio["Cherelles_avg"], 2) if promedio["Cherelles_avg"] else 0
            ),
        }
        for promedio in promedios
    ]
    data = OrderByVictoria(data)
    return data


def GetTreeTotal(hacienda_id):
    total_plantas = (
        Proyecto.objects.filter(
            Activo=True,
            lote__planta__VisibleToStudent=True,
            Id_Hacienda_id=hacienda_id,
        ).aggregate(TotalPlantas=Count("lote__planta"))["TotalPlantas"]
        or 0
    )

    return total_plantas


def NewUsers():
    return Perfil.objects.filter(Id_Hacienda__isnull=True).count()


def LecturasCurrentMonth(id_hacienda: int, now: datetime.date):
    mes_actual = now.month
    año_actual = now.year
    lecturas_mes = (
        Lectura.objects.select_related("Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda")
        .filter(
            Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda_id=id_hacienda,
            FechaVisita__month=mes_actual,
            FechaVisita__year=año_actual,
            Activo=True,
        )
        .count()
    )
    Plantas = GetTreeTotal(id_hacienda)
    if Plantas == 0:
        return 0
    print(Plantas)
    print(lecturas_mes)
    return round((lecturas_mes / Plantas) * 100, 2)


def LecturasCurrentMonthByProject(id_hacienda, now: datetime.date):
    mes_actual = now.month
    año_actual = now.year
    proyectos = Proyecto.objects.filter(Id_Hacienda_id=id_hacienda)
    data = []
    for proyecto in proyectos:
        lecturas_mes = (
            Lectura.objects.select_related(
                "Id_Planta__Id_Lote__Id_Proyecto__Id_Hacienda"
            )
            .filter(
                Id_Planta__Id_Lote__Id_Proyecto=proyecto,
                FechaVisita__month=mes_actual,
                FechaVisita__year=año_actual,
                Activo=True,
            )
            .count()
        )
        plantas = proyecto.lote_set.filter(planta__VisibleToStudent=True).count()
        if plantas == 0:
            continue
        porcentaje = round((lecturas_mes / plantas) * 100, 2)
        data.append({"Proyect": proyecto.Nombre, "Lecturas": porcentaje})
    return data
