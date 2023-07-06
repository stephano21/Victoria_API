from rest_framework import routers
from django.urls import path
from .views import ProyectoHaciendaAPIView,LoteAPIView, EstacionAPIView,PlantaAPIView
from .api import HaciendaViewSet, ProyectoViewSet, LecturaViewSet
router = routers.DefaultRouter()
router.register('api/hacienda', HaciendaViewSet)
router.register('api/proyectos', ProyectoViewSet)
#router.register('api/estaciones', EstacionViewSet)
#router.register('api/plantas', PlantaViewSet)
router.register('api/lecturas', LecturaViewSet)
#router.register('api/lotesTest', LoteAPIView, basename='lotesTest')
urlpatterns = [
    path('api/hacienda/<int:hacienda_id>/proyectos/', ProyectoHaciendaAPIView.as_view(), name='proyectos-hacienda'),
    # Otras rutas de la aplicación Hacienda
    path('api/lotes/', LoteAPIView.as_view(), name='lotes'),
    path('api/lotes/<int:id>/', LoteAPIView.as_view(), name='lotes'),
    path('api/lotes/details/<int:id>/', LoteAPIView.as_view(), name='lotes'),
    #estaciones
    path('api/estaciones/', EstacionAPIView.as_view(), name='estaciones'),
    path('api/estaciones/<int:id>/', EstacionAPIView.as_view(), name='estaciones'),
    #plantas
    path('api/plantas/', PlantaAPIView.as_view(), name='estaciones'),
    path('api/plantas/<int:id>/', PlantaAPIView.as_view(), name='estaciones'),
]
urlpatterns += router.urls
