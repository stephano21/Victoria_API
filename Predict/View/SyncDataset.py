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

from Predict.data.predictService import get_predict, predict, update_dataset_pred
from Predict.models import DatasetPred
from utils.Console import console
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class SyncDataset(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        try:
            
            hacienda = request.hacienda_id
            user = request.user
            username = user.username
            console.log(f"{username} esta actualizando el dataset de la hacienda {hacienda}")
            
            return Response( update_dataset_pred(hacienda), status=status.HTTP_200_OK)
        except Exception as e:
            console.error(e)
            return Response(f"Error al sincronizar el dataset:{str(e)}", status=status.HTTP_400_BAD_REQUEST)