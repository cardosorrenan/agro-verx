from django.core.exceptions import ValidationError
from rest_framework import serializers

from agro_verx.producer.models import ProducerModel

from .utils import validate_document_number


class ProducerSerializer(serializers.ModelSerializer):
    def validate(self, data):
        doc_type = data.get('producer_document_type', None)
        cpf_number = data.get('producer_cpf_number', None)
        cnpj_number = data.get('producer_cnpj_number', None)

        try:
            validate_document_number(
                document_type=doc_type,
                cpf_number=cpf_number if doc_type == 'CPF' else None,
                cnpj_number=cnpj_number if doc_type == 'CNPJ' else None,
            )
            return data
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    class Meta:
        model = ProducerModel
        fields = '__all__'
