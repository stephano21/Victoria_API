from ..models import Usuarios
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Realiza la autenticación del usuario
        user = Usuarios.objects.get(username=username)
        if user.check_password(password):
            # Genera los tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Retorna los tokens en la respuesta
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
 