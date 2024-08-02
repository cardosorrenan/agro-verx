from django.db import models
from django.utils.translation import gettext_lazy as _


class ProducerDocumentTypeEnum(models.TextChoices):
    CPF = 'CPF', _('CPF')
    CNPJ = 'CNPJ', _('CNPJ')
