# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from Users.serializers import AsignacionGrupoSerializer

class AsignarGrupoView(APIView):
    def post(self, request, format=None):
        serializer = AsignacionGrupoSerializer(data=request.data)
        if serializer.is_valid():
            usuario_id = request.data.get('usuario_id')
            grupo_id = request.data.get('grupo_id')
            try:
                usuario = User.objects.get(id=usuario_id)
                grupo = Group.objects.get(id=grupo_id)
                usuario.groups.add(grupo)
                usuario.save()
                return Response({"mensaje": "Grupo asignado con éxito"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"mensaje": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Group.DoesNotExist:
                return Response({"mensaje": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
