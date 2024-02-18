from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse
from decouple import config
class LogOutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print(config('CORS_ALLOWED_ORIGINS'))
        # Redirigir inmediatamente a la URL externa después de cerrar sesión
        return redirect(config('CORS_ALLOWED_ORIGINS'))  # Reemplaza con tu URL externa
   
