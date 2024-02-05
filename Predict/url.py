from rest_framework import routers
from django.urls import path
from Clima.views import SyncView,DataView,CargarDatosDesdeExcel,PandasView
router = routers.DefaultRouter()

urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/predict/', SyncView.as_view(), name='sync'),
]
urlpatterns += router.urls
