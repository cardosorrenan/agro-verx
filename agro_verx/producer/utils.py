import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProducerDocumentTypeEnum(models.TextChoices):
    CPF = 'CPF', _('CPF')
    CNPJ = 'CNPJ', _('CNPJ')


def validate_cpf(cpf_number):
    CPF_LENGTH = 14
    cpf_regex_pattern = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

    if not cpf_number:
        raise ValidationError(
            {'producer_cpf_number': "CPF number mustn't be empty."}
        )

    if len(cpf_number) != CPF_LENGTH:
        raise ValidationError(
            {
                'producer_cpf_number': f'CPF must be exactly {CPF_LENGTH} characters long.'
            }
        )

    if not re.match(cpf_regex_pattern, cpf_number):
        raise ValidationError(
            {
                'producer_cpf_number': 'Invalid CPF number. It should be in the format XXX.XXX.XXX-XX.'
            }
        )

    return True


def validate_cnpj(cnpj_number):
    CNPJ_LENGTH = 18
    cnpj_regex_pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'

    if not cnpj_number:
        raise ValidationError(
            {'producer_cnpj_number': "CNPJ number mustn't be empty."}
        )

    if len(cnpj_number) != CNPJ_LENGTH:
        raise ValidationError(
            {
                'producer_cnpj_number': f'CNPJ must be exactly {CNPJ_LENGTH} characters long.'
            }
        )

    if not re.match(cnpj_regex_pattern, cnpj_number):
        raise ValidationError(
            {
                'producer_cnpj_number': 'Invalid CNPJ number. It should be in the format XX.XXX.XXX/XXXX-XX.'
            }
        )

    return True


def validate_document_number(document_type, cpf_number=None, cnpj_number=None):
    if document_type == 'CPF':
        return validate_cpf(cpf_number)
    elif document_type == 'CNPJ':
        return validate_cnpj(cnpj_number)
    else:
        raise ValidationError("Invalid document type. Must be CPF or CNPJ'.")
