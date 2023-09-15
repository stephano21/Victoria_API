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
from Clima.Arable.Auth import GetData, Login, BuidlSerializer


class DataView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):        
        Data = Daily_Indicadores.objects.order_by('Date')
        serializer = DailyIndicadorSerializers(Data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)