from rest_framework import routers
from django.urls import path
from Clima.views import SyncView,DataView,CargarDatosDesdeExcel
router = routers.DefaultRouter()

urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/weather/sync/', SyncView.as_view(), name='sync'),
    path('api/weather/data/', DataView.as_view(), name='data'),
    path('api/weather/upload', CargarDatosDesdeExcel.as_view(), name='file'),
]
urlpatterns += router.urls
