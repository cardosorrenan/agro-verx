from django.core.exceptions import ValidationError
from rest_framework import serializers

from agro_verx.core.serializers import CoreCitySerializer
from agro_verx.producer.models import (
    ProducerFarmModel,
    ProducerFarmPlantationModel,
    ProducerModel,
    ProducerPlantationTypeModel,
)

from .utils import validate_document_number


class ProducerSerializer(serializers.ModelSerializer):
    def validate(self, data):
        self._validate_document_number(data)
        return data

    def _validate_document_number(self, data):
        request = self.context.get('request')
        partial = request and request.method == 'PATCH'

        doc_type = data.get(
            'producer_document_type',
            self.instance.producer_document_type if partial else None,
        )
        cpf_number = data.get(
            'producer_cpf_number',
            self.instance.producer_cpf_number if partial else None,
        )
        cnpj_number = data.get(
            'producer_cnpj_number',
            self.instance.producer_cnpj_number if partial else None,
        )

        try:
            validate_document_number(
                document_type=doc_type,
                cpf_number=cpf_number if doc_type == 'CPF' else None,
                cnpj_number=cnpj_number if doc_type == 'CNPJ' else None,
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    class Meta:
        model = ProducerModel
        fields = '__all__'


class ProducerFarmSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        city_id = instance.city_id
        if city_id:
            representation['city_id'] = CoreCitySerializer(city_id).data

        producer_id = instance.producer_id
        if producer_id:
            representation['producer_id'] = ProducerSerializer(
                producer_id
            ).data
        return representation

    def validate(self, data):

        self._validate_area_constraints(data)
        return data

    def _validate_area_constraints(self, data):
        request = self.context.get('request')
        partial = request and request.method == 'PATCH'
        total_area = data.get(
            'total_area_hectares',
            self.instance.total_area_hectares if partial else None,
        )
        arable_area = data.get(
            'arable_area_hectares',
            self.instance.arable_area_hectares if partial else None,
        )
        vegetation_area = data.get(
            'vegetation_area_hectares',
            self.instance.vegetation_area_hectares if partial else None,
        )

        if (arable_area + vegetation_area) > total_area:
            raise serializers.ValidationError(
                'The sum of arable area and vegetation area cannot exceed the total area.'
            )

    class Meta:
        model = ProducerFarmModel
        exclude = ('plantations',)


class PlantationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerPlantationTypeModel
        fields = '__all__'


class ProducerFarmPlantationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['plantation_type_id'] = PlantationTypeSerializer(
            instance.plantation_type_id
        ).data

        representation['farm_id'] = ProducerFarmSerializer(
            instance.farm_id
        ).data
        return representation

    class Meta:
        model = ProducerFarmPlantationModel
        fields = '__all__'
