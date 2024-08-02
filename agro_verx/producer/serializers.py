from rest_framework import serializers

from agro_verx.producer.models import ProducerModel


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerModel
