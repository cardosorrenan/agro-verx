from django.urls import include, path
from rest_framework import routers

from .views import DashboardHomeViewset

router = routers.DefaultRouter()

router.register(r'home', DashboardHomeViewset, basename='dashboard-home')

urlpatterns = [
    path('', include(router.urls)),
]
