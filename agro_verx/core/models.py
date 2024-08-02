from django.db import models


class CoreStateModel(models.Model):
    state_id = models.BigAutoField(primary_key=True, db_column="state_id")
    state_name = models.CharField(max_length=255, unique=True, db_column="state_name")
    state_abbreviation = models.CharField(
        max_length=2, unique=True, db_column="state_abbreviation"
    )

    class Meta:
        db_table = "core_state"
        verbose_name = "State"
        verbose_name_plural = "States"


class CoreCityModel(models.Model):
    city_id = models.BigAutoField(primary_key=True, db_column="city_id")
    city_name = models.CharField(max_length=255, db_column="city_name")
    state_id = models.ForeignKey(
        CoreStateModel,
        on_delete=models.PROTECT,
        db_column="state_id",
        related_name="cities",
    )

    class Meta:
        db_table = "core_city"
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("city_name", "state_id")
