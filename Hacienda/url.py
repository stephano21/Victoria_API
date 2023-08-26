from rest_framework import routers
from django.urls import path
from .views import LoteAPIView,ProyectoHaciendaAPIView,GeoLotesView
from .api import HaciendaViewSet, ProyectoViewSet, LecturaViewSet
router = routers.DefaultRouter()
router.register('api/hacienda', HaciendaViewSet)
router.register('api/proyectos', ProyectoViewSet)
router.register('api/lecturas', LecturaViewSet)
urlpatterns = [
    path('api/hacienda/<int:hacienda_id>/proyectos/', ProyectoHaciendaAPIView.as_view(), name='proyectos-hacienda'),
    # Otras rutas de la aplicación Hacienda
    path('api/lotes/', LoteAPIView.as_view(), name='lotes'),
    path('api/lotes/<int:id>/', LoteAPIView.as_view(), name='lotes'),
    path('api/lotes/details/<int:id>/', LoteAPIView.as_view(), name='lotes'),
    #path('api/login/', LoginView.as_view(), name='login'),
    #path('api/register/', RegisterView.as_view(), name='register'),
    path('api/geolotes/', GeoLotesView.as_view(), name='geolotes'),
    #path('api/geolotes/<int:id>/', GeoLotesView.as_view(), name='geolotes'),
]
urlpatterns += router.urls
