from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from django.db.models import Count, F, QuerySet, Sum

from agro_verx.producer.models import (
    ProducerFarmModel,
    ProducerFarmPlantationModel,
)


@dataclass
class DashboardStats:
    """
    Dataclass to hold dashboard statistics.

    Attributes:
        amount_farms (int): Total number of farms.
        amount_hectare_farms (float): Total area of farms in hectares.
        farms_states_pizza (List[Dict[str, Any]]): Farm count by state.
        plantations_farms (List[Dict[str, Any]]): Plantation count by type.
        farms_percentage_area (Dict[str, float]): Farm area percentages.
    """

    amount_farms: int
    amount_hectare_farms: float
    farms_states_pizza: List[Dict[str, Any]]
    plantations_farms_pizza: List[Dict[str, Any]]
    farms_percentage_area_pizza: Dict[str, float]


class DashboardService:
    """
    Service class to generate dashboard statistics for farms and plantations.
    """

    def __init__(self):
        """Initialize the DashboardService with queryset for farms and plantations."""
        self.farms_qs: QuerySet = ProducerFarmModel.objects.all()
        self.plantations_farms_qs: QuerySet = (
            ProducerFarmPlantationModel.objects.all()
        )

    def get_dashboard_home_result(self) -> Dict[str, Any]:
        """
        Retrieve all dashboard statistics.

        Returns:
            Dict[str, Any]: A dictionary containing all calculated dashboard statistics.
        """
        dashboard_stats = DashboardStats(
            amount_farms=self._get_farm_count(),
            amount_hectare_farms=self._get_total_farm_area(),
            farms_states_pizza=self._get_farms_by_state(),
            plantations_farms_pizza=self._get_plantations_by_type(),
            farms_percentage_area_pizza=self._get_farm_area_percentages(),
        )
        return asdict(dashboard_stats)

    def _get_farm_count(self) -> int:
        """
        Get the total number of farms.

        Returns:
            int: Total number of farms.
        """
        return self.farms_qs.count()

    def _get_total_farm_area(self) -> float:
        """
        Calculate the total area of all farms in hectares.

        Returns:
            float: Total farm area in hectares.
        """
        return (
            self.farms_qs.aggregate(total_area=Sum('total_area_hectares'))[
                'total_area'
            ]
            or 0
        )

    def _get_farms_by_state(self) -> List[Dict[str, Any]]:
        """
        Get the count of farms grouped by state.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing state information and farm count.
        """
        return list(
            self.farms_qs.select_related('city_id__state_id')
            .values(
                state_name=F('city_id__state_id__state_name'),
                state_id=F('city_id__state_id__state_id'),
            )
            .annotate(count=Count('id'))
            .order_by('-count')
        )

    def _get_plantations_by_type(self) -> List[Dict[str, Any]]:
        """
        Get the count of plantations grouped by plantation type.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing plantation type and count.
        """
        return list(
            self.plantations_farms_qs.select_related('plantation_type_id')
            .values(plantation_type=F('plantation_type_id__plantation_type'))
            .annotate(count=Count('farm_id'))
            .order_by('-count')
        )

    def _get_farm_area_percentages(self) -> Dict[str, float]:
        """
        Calculate the total vegetation and arable areas of all farms.

        Returns:
            Dict[str, float]: Dictionary containing total vegetation and arable areas.
        """
        return self.farms_qs.aggregate(
            vegetation_area_hectares=Sum('vegetation_area_hectares'),
            arable_area_hectares=Sum('arable_area_hectares'),
        )
