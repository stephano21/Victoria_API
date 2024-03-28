from rest_framework import routers
from django.urls import path
from Predict.View.PredictedView import PredictedView
router = routers.DefaultRouter()

urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/predict/', PredictedView.as_view(), name='sync'),
]
urlpatterns += router.urls
