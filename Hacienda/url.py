from rest_framework import routers
from django.urls import path
from .views import ProyectoHaciendaAPIView
from .api import HaciendaViewSet, ProyectoViewSet, LoteViewSet, EstacionViewSet, PlantaViewSet, LecturaViewSet
router = routers.DefaultRouter()
router.register('api/hacienda', HaciendaViewSet)
router.register('api/proyectos', ProyectoViewSet)
router.register('api/lotes', LoteViewSet)
router.register('api/estaciones', EstacionViewSet)
router.register('api/plantas', PlantaViewSet)
router.register('api/lecturas', LecturaViewSet)
urlpatterns = [
    path('api/hacienda/<int:hacienda_id>/proyectos/', ProyectoHaciendaAPIView.as_view(), name='proyectos-hacienda'),
    # Otras rutas de la aplicación Hacienda
]
urlpatterns += router.urls
