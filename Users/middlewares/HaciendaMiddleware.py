# middlewares.py

from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.models import Perfil
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from decouple import config
from django.contrib.auth.models import User
class HaciendaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verificar si el usuario está autenticado
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                idUser = self.ValidateToken(token)
                if idUser>0 :
                    try:
                        # Obtener el perfil asociado al usuario
                        perfil = Perfil.objects.get(user_id=idUser)
                        Roles = User.objects.get(pk=idUser).groups.all()
                        first_group_name = Roles.last().name if Roles else None
                        print(perfil)
                        print(first_group_name)
                        # Establecer el ID de la hacienda en el contexto de la solicitud
                        request.hacienda_id = perfil.Id_Hacienda.id if perfil.Id_Hacienda else None
                        request.rol = first_group_name if first_group_name else ""
                    except Perfil.DoesNotExist:
                        # Manejar el caso en que el perfil no existe para el usuario
                        request.hacienda_id = None
                        request.rol = ""
                else:
                    # Usuario no autenticado, establecer hacienda_id como None
                    request.hacienda_id = None
                    request.rol = ""
        else:
            # No hay encabezado de autorización, establecer hacienda_id como None
            request.hacienda_id = None
            request.rol = ""

    def ValidateToken(self, token):
        SECRET_KEY = config('SECRET_KEY')
        try:
            # Decodificar el token JWT y verificar la firma
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # En este punto, el token ha sido decodificado y la firma es válida
            # Puedes acceder a la información del usuario y otros datos del token, por ejemplo:
            user_id = decoded_token['user_id']
            #username = decoded_token['username']
            print(f"Token válido para el usuario  con ID {user_id}")
            return user_id
        except ExpiredSignatureError:
            print("El token ha expirado")
            return 0
        except DecodeError:
            print("Error al decodificar el token")
            return 0
