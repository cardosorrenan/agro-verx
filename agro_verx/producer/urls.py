from django.urls import include, path
from rest_framework import routers

from .views import (
    ProducerFarmPlantationViewSet,
    ProducerFarmViewSet,
    ProducerViewset,
)

router = routers.DefaultRouter()

router.register(
    r'producer',
    ProducerViewset,
)
router.register(r'farm-plantation', ProducerFarmPlantationViewSet)
router.register(r'farm', ProducerFarmViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
