from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from agro_verx.producer.models import (
    ProducerFarmModel,
    ProducerFarmPlantationModel,
    ProducerModel,
)
from agro_verx.producer.serializers import (
    ProducerFarmPlantationSerializer,
    ProducerFarmSerializer,
    ProducerSerializer,
)


class ProducerViewset(viewsets.ModelViewSet):
    queryset = ProducerModel.objects.all()
    serializer_class = ProducerSerializer

    @action(detail=True, methods=['patch'], url_path='restore')
    def restore(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = ProducerModel.all_objects.get(pk=pk)
        except ProducerModel.DoesNotExist:
            return Response(
                {'detail': 'Producer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        instance.restore()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProducerFarmPlantationViewSet(viewsets.ModelViewSet):
    queryset = ProducerFarmPlantationModel.objects.filter(
        farm_id__producer_id__is_deleted=False
    )
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ProducerFarmPlantationSerializer

    def get_queryset(self):
        return ProducerFarmPlantationModel.objects.filter(
            farm_id__producer_id__is_deleted=False
        )


class ProducerFarmViewSet(viewsets.ModelViewSet):
    queryset = ProducerFarmModel.objects.filter(producer_id__is_deleted=False)
    serializer_class = ProducerFarmSerializer
