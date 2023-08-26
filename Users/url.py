from rest_framework import routers
from django.urls import path
from Users.views import LoginView, RegisterView
router = routers.DefaultRouter()
urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
]
urlpatterns += router.urls