from datetime import datetime
from Hacienda.models import Hacienda, Produccion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import ProduccionSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.AnalyticsData import LecturasCurrentMonth, NewUsers, LecturasCurrentMonthByProject
from utils.Console import console


class HomeInfoView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...

    def get(self, request, *args, **kwargs):
        user = request.user
        username = user.username
        Rol = request.rol
        print(f"{username} Ha ingresado al menu principal")
        date = datetime.now().date()
        #date = "2023-12-01"
        #date = datetime.strptime(date, "%Y-%m-%d").date()
        new_date = datetime.combine(date, datetime.min.time())
        console.log(type(new_date))
        console.log(date)
        if Rol in ["Root", "Researcher"]:
            haciendas_activas = Hacienda.objects.filter(Activo=True)
            console.warn(f"Root or Researcher: {haciendas_activas}")
            haciendas = []
            for hacienda in haciendas_activas:
                haciendas.append({
                    'Hacienda': hacienda.Nombre,
                    'Lecturas': LecturasCurrentMonth(hacienda.id, date),
                    'Proyects': LecturasCurrentMonthByProject(hacienda.id, date),
                })
            data = {
                'Date': str(date),
                'Usuarios': NewUsers(),
                'Haciendas': haciendas
            }
            return Response(data)
        id_hacienda = request.hacienda_id
        # Obtener el parámetro de la URL 'fecha'
        From, To = "", ""
        if request.query_params.get('from'):
            From = request.query_params.get('from')
        if request.query_params.get('to'):
            To = request.query_params.get('to')

        data = {
            'Date': str(date),
            'Usuarios': NewUsers(),
            'Lecturas': LecturasCurrentMonth(id_hacienda, date),
            'Haciendas': [{
                'Hacienda': Hacienda.objects.get(id=id_hacienda).Nombre,
                'Lecturas': LecturasCurrentMonth(id_hacienda, date),
                'Proyects': LecturasCurrentMonthByProject(id_hacienda, date),
            }]
        }
        return Response(data)
