from rest_framework import routers
from django.urls import path
from Hacienda.views import (LoteAPIView,
                            GeoLotesView,
                            LecturaAPIView,
                            PlantaAPIView,
                            ImportLecturas,
                            ProduccionAPIView,
                            ImportProduccion,
                            ImportLotesView,
                            ImportPlantasView,
                            EstadisticasView,
                            HomeInfoView,
                            ProyectoAPIView,)
from Hacienda.api import HaciendaViewSet  # , LecturaViewSet
router = routers.DefaultRouter()
router.register('api/hacienda', HaciendaViewSet)
urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/proyectos/', ProyectoAPIView.as_view(), name='proyectos'),
    path('api/proyectos/<int:id>/', ProyectoAPIView.as_view(), name='proyectos'),
    path('api/lotes/', LoteAPIView.as_view(), name='lotes'),
    path('api/lotes/upload', ImportLotesView.as_view(), name='lotes'),
    path('api/lotes/<int:id>/', LoteAPIView.as_view(), name='lotes'),
    path('api/geolotes/', GeoLotesView.as_view(), name='geolotes'),
    path('api/geolotes/<int:id>/', GeoLotesView.as_view(), name='geolotes'),
    path('api/lecturas/', LecturaAPIView.as_view(), name='lecturas'),
    path('api/lecturas/upload', ImportLecturas.as_view(), name='lecturas'),
    path('api/plantas/', PlantaAPIView.as_view(), name='plantas'),
    path('api/plantas/<int:id>/', PlantaAPIView.as_view(), name='plantas'),
    path('api/plantas/upload', ImportPlantasView.as_view(), name='plantas'),
    path('api/produccion/', ProduccionAPIView.as_view(), name='produccion'),
    path('api/produccion/upload', ImportProduccion.as_view(), name='Produccion'),
    path('api/analytics/', EstadisticasView.as_view(), name='Analytics'),
    path('api/analytics/home', HomeInfoView.as_view(), name='Analytics'),
]
urlpatterns += router.urls
