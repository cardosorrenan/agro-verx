from rest_framework import viewsets

from agro_verx.producer.models import ProducerModel, ProducerPlantationModel
from agro_verx.producer.serializers import (
    ProducerPlantationSerializer,
    ProducerSerializer,
)


class ProducerViewset(viewsets.ModelViewSet):
    queryset = ProducerModel.objects.all()
    serializer_class = ProducerSerializer


class ProducerPlantationViewSet(viewsets.ModelViewSet):
    queryset = ProducerPlantationModel.objects.all()
    serializer_class = ProducerPlantationSerializer
