from rest_framework import routers
from django.urls import path
from Users.views import LoginView, RegisterView,RefreshTokenView
router = routers.DefaultRouter()
urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/refresh/', RefreshTokenView.as_view(), name='refresh'),
]
urlpatterns += router.urls