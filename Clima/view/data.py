from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Clima.models import Daily_Indicadores
from Clima.serializers import DailyIndicadorSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from Clima.Arable.Predict import GenerateDF, predict, GetWeather, GetLecturasv1, getProduction
from Predict.models import Dataset
from datetime import datetime, timedelta


class PandasView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hacienda = request.hacienda_id
        dataset_exists = Dataset.objects.filter(
            Id_Lote__Id_Proyecto__Id_Hacienda=hacienda, date=datetime.now().date()).exists()
        if not dataset_exists:
            Data = predict(hacienda,datetime.now())
            return Response(Data, status=status.HTTP_200_OK)
        else:
            return Response("No se encontró un dataset para la fecha actual", status=status.HTTP_404_NOT_FOUND)
