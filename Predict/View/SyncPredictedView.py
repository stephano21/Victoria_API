from Clima.Arable.Auth import GetData, Login, BuidlSerializer, Current_Data, Current_Date
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Clima.models import Daily_Indicadores
from Clima.serializers import DailyIndicadorSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Predict.data.predictService import get_predict, predict
from Predict.models import DatasetPred
from utils.Console import console
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class SyncPredictedView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            hacienda = request.hacienda_id
            user = request.user
            username = user.username
            datecreate = datetime(year=2024, month=2, day=15)
            dataset_exists = DatasetPred.objects.filter(
                Id_Lote__Id_Proyecto__Id_Hacienda=hacienda, date=datecreate.date()).exists()
            console.log(f"Dataset exists: {not dataset_exists}")
            if False == False:
                console.log("aqui")
                Data = predict(hacienda,datecreate,username)
                
                return Response("Sincronizado exitosamente!", status=status.HTTP_200_OK)
            else:
                console.log("aqui")
                return Response("No se encontró un dataset para la fecha actual", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            console.error(e)
            return Response(f"Error al sincronizar el dataset:{str(e)}", status=status.HTTP_400_BAD_REQUEST)
