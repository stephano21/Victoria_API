from Hacienda.models import Produccion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import ProduccionSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class ProduccionAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        user = request.user
        username = user.username
        print(f"{username} Ha cargado Qintales producidos")
        id = self.kwargs.get('id')
        if id: 
            Produccions = Produccion.objects.filter(Id_Lote = id , Activo=True)
            serializer = ProduccionSerializers(Produccions, many=True)
            return Response(serializer.data)

        produccion = Produccion.objects.filter(Activo=True)
        serializer = ProduccionSerializers(produccion, many=True)
        return Response(serializer.data)
    def post(self, request):
        user = request.user
        username = user.username
        print(f"{username} Ha registrado una Produccion")
        serializer = ProduccionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        Produccion = self.get_object(pk)
        serializer = ProduccionSerializers(Produccion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Produccion.objects.get(pk=pk)
        except Produccion.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request, id):
        Produccion = self.get_object(id)
        Produccion.Activo = False
        Produccion.save()

        serializer = ProduccionSerializers(Produccion)
        return Response(serializer.data)
