from Hacienda.models import Produccion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import ProduccionSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.AnalyticsData import LecturasCurrentMonth, NewUsers

class HomeInfoView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        user = request.user
        username = user.username
        print(f"{username} Ha ingresado al menu principal")
        id_hacienda = request.hacienda_id 
        
        # Obtener el parámetro de la URL 'fecha'
        From,To = "",""
        if request.query_params.get('from'):
            From= request.query_params.get('from')
        if request.query_params.get('to'):
           To =request.query_params.get('to')
        
        print( type(From) )
        
        data={
            'Usuarios':NewUsers(),
            'lecturas': LecturasCurrentMonth(id_hacienda),
        }
        return Response(data)
   
