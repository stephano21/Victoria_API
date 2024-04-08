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

from Predict.data.predictService import predict
from Predict.models import DatasetPred
from utils.Console import console
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class PredictedView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hacienda = request.hacienda_id
        user = request.user
        username = user.username
        dataset_exists = DatasetPred.objects.filter(
            Id_Lote__Id_Proyecto__Id_Hacienda=hacienda, date=datetime.now().date()).exists()
        console.log(f"Dataset exists: {dataset_exists}")
        if not dataset_exists:
            Data = predict(hacienda,datetime.now(),username)
            return Response(Data, status=status.HTTP_200_OK)
        else:
            return Response("No se encontró un dataset para la fecha actual", status=status.HTTP_404_NOT_FOUND)
