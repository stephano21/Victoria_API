from Hacienda.models import Lectura
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Hacienda.serializers import LecturaSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class LecturaAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Código existente...
    def get(self, request,*args, **kwargs):
        id = self.kwargs.get('id')
        if id: 
            lecturas = Lectura.objects.filter(Id_Lectura = id)
            serializer = LecturaSerializers(lecturas, many=True)
            return Response(serializer.data)

        lecturas = Lectura.objects.all()
        serializer = LecturaSerializers(lecturas, many=True)
        return Response(serializer.data)
    def post(self, request):
        username = request.user.username
        print(username)
        request.data['username'] = username
        serializer = LecturaSerializers(data=request.data)
        serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Lectura.objects.get(pk=pk)
        except Lectura.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete (self, request, id):
        lectura = self.get_object(id)
        lectura.Activo = False
        lectura.save()

        serializer = LecturaSerializers(lectura)
        return Response(serializer.data)