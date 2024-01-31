from Hacienda.models import Produccion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import ProduccionSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.AnalyticsData import GertTreeByLot, GetLecturasPerMonth

class EstadisticasView(APIView):
    #authentication_classes = [SessionAuthentication, JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        user = request.user
        # Obtener el parámetro de la URL 'fecha'
        From,To = "",""
        if request.query_params.get('from'):
            From= request.query_params.get('from')
        if request.query_params.get('to'):
           To =request.query_params.get('to')
        
        print( type(From) )
        username = user.username
        print(f"{username} Ha cargado Qintales producidos")
        Lecturas = GetLecturasPerMonth(From,To)
        Trees = GertTreeByLot()
        data={
            'Trees':Trees,
            'Lecturas':Lecturas,
        }
        return Response(data)
   
