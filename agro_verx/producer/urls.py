from django.urls import include, path
from rest_framework import routers

from .views import ProducerPlantationViewSet, ProducerViewset

router = routers.DefaultRouter()

router.register(
    r'producer',
    ProducerViewset,
)
router.register(r'producer-plantation', ProducerPlantationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
