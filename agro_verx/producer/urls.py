from django.urls import include, path
from rest_framework import routers

from .views import ProducerViewset

router = routers.DefaultRouter()

router.register(
    r'/producer',
    ProducerViewset,
)

urlpatterns = [
    path('', include(router.urls)),
]
