from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Clima.models import Daily_Indicadores
from Clima.serializers import DailyIndicadorSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from Clima.Arable.TransformData import GetData, getLotes
class PandasView(APIView):
    def get(self, request):        
        Data = getLotes()
        return Response("testt", status=status.HTTP_200_OK)