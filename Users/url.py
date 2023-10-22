from rest_framework import routers
from django.urls import path
from Users.views import LoginView, RegisterView,RefreshTokenView,PorfileView,ImportUsers
router = routers.DefaultRouter()
urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('api/auth/porfile/', PorfileView.as_view(), name='porfile'),
    path('api/auth/register/import', ImportUsers.as_view(), name='ImportUsers'),
]
urlpatterns += router.urls