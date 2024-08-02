from django.urls import include, path

urlpatterns = [path('api/producer', include('agro_verx.producer.urls'))]
