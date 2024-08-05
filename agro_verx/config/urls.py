from django.urls import include, path

from . import yasg_schema

urlpatterns = [
    path('v1/api/producer/', include('agro_verx.producer.urls')),
    path('v1/api/dashboard/', include('agro_verx.dashboard.urls')),
]

urlpatterns += yasg_schema.urlpatterns
