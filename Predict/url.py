from rest_framework import routers
from django.urls import path
from Predict.views import PredictedView, SyncPredictedView, SyncDataset
router = routers.DefaultRouter()

urlpatterns = [
    # Otras rutas de la aplicación Hacienda
    path('api/predict/', PredictedView.as_view(), name='predict'),
    path('api/predict/sync/', SyncPredictedView.as_view(), name='sync'),
    path('api/predict/dataset/sync/', SyncDataset.as_view(), name='sync'),
]
urlpatterns += router.urls
