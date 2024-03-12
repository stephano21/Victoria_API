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
"""Document by SWAGGER"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
"""
Arable data
"""


class PredictedView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        username = user.username
        print(Current_Data())
        if not Current_Data():
            token = Login()
            start_time = Current_Date()
            print(start_time)
            if isinstance(start_time, datetime):
                data = GetData(token, start_time.date())
            else:
                data = GetData(token)
            if data == "":
                return Response("Ocurrió un error con arable!", status=status.HTTP_400_BAD_REQUEST)
            Format_Data = BuidlSerializer(data, username)
            # Validar si Format_Data es un arreglo de objetos
            if not isinstance(Format_Data, list) or not all(isinstance(i, dict) for i in Format_Data):
                return Response(Format_Data, status=status.HTTP_400_BAD_REQUEST)
            # Pasar al serializador
            DailyIndicadoresSerializers = [DailyIndicadorSerializers(
                data=data) for data in Format_Data]
            # Validar que todos los objetos esten correctos
            for serializer in DailyIndicadoresSerializers:
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            registros_sincronizados = 0
            for serializer in DailyIndicadoresSerializers:
                if serializer.is_valid():
                    serializer.save()
                    registros_sincronizados += 1
            return Response(f"Se han sincronizado {registros_sincronizados} registros exitosamente!", status=status.HTTP_200_OK)
        return Response("Los datos ya se han sincronizado!", status=status.HTTP_200_OK)
