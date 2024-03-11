import uuid
from Hacienda.models import Lote
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import LoteSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from Hacienda.validators.ValidatorHelper import GetIdLote

class LoteAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        user = request.user
        hacienda = request.hacienda_id 
        username = user.username
        print(f"{username} Ha cargado lotes")
        id = self.kwargs.get('id')
        Rol = request.rol
        if hacienda and Rol != "Researcher":
            if id: 
                lotes = Lote.objects.select_related('Id_Proyecto__Id_Hacienda').filter(
                    Id_Proyecto = id,
                    Activo=True,
                    Id_Proyecto__Id_Hacienda_id=hacienda)
                serializer = LoteSerializers(lotes, many=True)
                return Response(serializer.data)
            lotes = Lote.objects.select_related('Id_Proyecto__Id_Hacienda').filter(
                Activo=True,
                Id_Proyecto__Id_Hacienda_id=hacienda) 
        else:
            lotes = Lote.objects.select_related('Id_Proyecto__Id_Hacienda').filter(
                Activo=True) 
        serializer = LoteSerializers(lotes, many=True)
        return Response(serializer.data)
    def post(self, request):
        user = request.user
        hacienda = request.hacienda_id
        username = user.username
        hacienda = request.hacienda_id
        existeLote = GetIdLote(request.data['Codigo_Lote'].strip(),hacienda)
        
        if existeLote: return Response( f"El lote {request.data['Codigo_Lote']} ya existe!", status=status.HTTP_400_BAD_REQUEST)
        request.data['poligonos'] = [
                        {
                            'FillColor': '#'+str(uuid.uuid4().hex[:6]),
                            'Usuario': str(username)
                        }
                    ]
        serializer = LoteSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        lote = self.get_object(pk)
        serializer = LoteSerializers(lote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(f"Lote {lote.Codigo_Lote} actualizado con éxito!", status=status.HTTP_200_OK)  # Return the serialized lote object
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Lote.objects.get(pk=pk)
        except Lote.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request,id):
        lote = self.get_object(id)
        lote.Activo = False
        lote.save()

        serializer = LoteSerializers(lote)
        return Response(f"Se ha eliminado el lote {lote.Codigo_Lote}",status=status.HTTP_200_OK)
