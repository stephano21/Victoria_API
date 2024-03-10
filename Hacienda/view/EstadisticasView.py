from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.AnalyticsData import GertTreeByLot, GetLecturasPerMonth, GetProductionByVictoria
class EstadisticasView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        user = request.user
        hacienda_id = request.hacienda_id
        print(hacienda_id)

        # Obtener el parámetro de la URL 'fecha'
        From,To = "",""
        if request.query_params.get('from'):
            From= request.query_params.get('from')
        if request.query_params.get('to'):
            To =request.query_params.get('to')
        
        print( type(From) )
        username = user.username
        print(f"{username} Ha cargado Estadisticas")
        data={
            'Trees':GertTreeByLot(hacienda_id),
            'Lecturas':GetLecturasPerMonth(From,To,hacienda_id),
            'Produccion':GetProductionByVictoria(From, To,hacienda_id),
        }
        return Response(data)

