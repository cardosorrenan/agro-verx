from django.core.exceptions import ValidationError
from rest_framework import serializers

from agro_verx.producer.models import ProducerModel

from .utils import validate_document_number


class ProducerSerializer(serializers.ModelSerializer):
    def validate(self, data):
        self._validate_document_number(data)
        self._validate_area_constraints(data)
        return data

    def _validate_document_number(self, data):
        doc_type = data.get('producer_document_type')
        cpf_number = data.get('producer_cpf_number')
        cnpj_number = data.get('producer_cnpj_number')

        try:
            validate_document_number(
                document_type=doc_type,
                cpf_number=cpf_number if doc_type == 'CPF' else None,
                cnpj_number=cnpj_number if doc_type == 'CNPJ' else None,
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def _validate_area_constraints(self, data):
        total_area = data.get('total_area_hectares', 0)
        arable_area = data.get('arable_area_hectares', 0)
        vegetation_area = data.get('vegetation_area_hectares', 0)

        if (arable_area + vegetation_area) <= total_area:
            raise serializers.ValidationError(
                'The sum of arable_area_hectares and vegetation_area_hectares cannot exceed total_area_hectares.'
            )

    class Meta:
        model = ProducerModel
        fields = '__all__'
