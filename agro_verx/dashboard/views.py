from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from agro_verx.dashboard.dashboard import DashboardService


class DashboardHomeViewset(GenericViewSet, ListModelMixin):
    service = DashboardService()

    def list(self, request, *args, **kwargs):
        results = self.service.get_dashboard_home_result()
        return Response(results, status=status.HTTP_200_OK)
