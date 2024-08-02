from rest_framework import viewsets

from agro_verx.producer.models import ProducerModel
from agro_verx.producer.serializers import ProducerSerializer


class ProducerViewset(viewsets.ModelViewSet):
    queryset = ProducerModel.objects.all()
    serializer_class = ProducerSerializer
