from django.db import models

from agro_verx.core.models import CoreCityModel
from agro_verx.producer.utils import ProducerDocumentTypeEnum


class ProducerPlantationTypeModel(models.Model):
    plantation_type_id = models.BigAutoField(
        primary_key=True, db_column='plantation_type_id'
    )
    plantation_type = models.CharField(
        max_length=50, unique=True, db_column='plantation_type'
    )

    class Meta:
        db_table = 'producer_plantation_type'
        verbose_name = 'Plantation Type'
        verbose_name_plural = 'Plantation Types'


class ProducerModel(models.Model):
    producer_id = models.BigAutoField(
        primary_key=True, db_column='producer_id'
    )
    producer_name = models.CharField(max_length=255, db_column='producer_name')
    producer_document_type = models.CharField(
        max_length=4,
        choices=ProducerDocumentTypeEnum,
        db_column='producer_document_type',
    )
    producer_cpf_number = models.CharField(
        max_length=14,
        null=True,
        db_column='producer_cpf_number',
    )
    producer_cnpj_number = models.CharField(
        max_length=18,
        null=True,
        db_column='producer_cnpj_number',
    )
    farm_name = models.CharField(max_length=128, db_column='farm_name')

    total_area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='total_area_hectares',
    )
    arable_area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='arable_area_hectares',
    )
    vegetation_area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='vegetation_area',
    )

    plantations = models.ManyToManyField(
        ProducerPlantationTypeModel, through='ProducerPlantationModel'
    )

    city_id = models.ForeignKey(
        CoreCityModel,
        on_delete=models.PROTECT,
        null=True,
        db_column='city_id',
        related_name='producers',
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_column='created_at'
    )
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()

    class Meta:
        db_table = 'producer_producer'
        verbose_name = 'Producer'
        verbose_name_plural = 'Producers'


class ProducerPlantationModel(models.Model):
    producer_plantation_id = models.BigAutoField(
        primary_key=True, db_column='producer_plantation_id'
    )
    plantation_type_id = models.ForeignKey(
        ProducerPlantationTypeModel,
        on_delete=models.CASCADE,
        db_column='plantation_type_id',
        related_name='plantation_types',
    )

    producer_id = models.ForeignKey(
        ProducerModel,
        on_delete=models.CASCADE,
        db_column='producer_id',
        related_name='producers',
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_column='producer_plantation_created_at'
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_column='producer_plantation_updated_at'
    )

    class Meta:
        db_table = 'producer_producer_plantation_type'
        verbose_name = 'Producer Platantions Types'
