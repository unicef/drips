from rest_framework import viewsets

from drips.api.filters import CostCenterFilter
from drips.api.serializers.cost_centers import CostCenterSerializer
from drips.api.views.base import GenericAbstractViewSetMixin
from drips.apps.cost_centers.models import CostCenter


class CostCenterViewSet(GenericAbstractViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer
    filterset_class = CostCenterFilter
    search_fields = ('description', 'code')
