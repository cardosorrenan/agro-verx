from rest_framework import serializers

from .models import CoreCityModel, CoreStateModel


class CoreStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreStateModel
        fields = '__all__'


class CoreCitySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['state_id'] = CoreStateSerializer(
            instance.state_id
        ).data
        return representation

    class Meta:
        model = CoreCityModel
        fields = '__all__'
