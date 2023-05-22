from rest_framework import routers
from .api import HaciendaViewSet, ProyectoViewSet, LoteViewSet, EstacionViewSet, PlantaViewSet, LecturaViewSet
router = routers.DefaultRouter()
router.register('api/hacienda', HaciendaViewSet)
router.register('api/proyectos', ProyectoViewSet)
router.register('api/lotes', LoteViewSet)
router.register('api/estaciones', EstacionViewSet)
router.register('api/plantas', PlantaViewSet)
router.register('api/lecturas', LecturaViewSet)
urlpatterns = router.urls

