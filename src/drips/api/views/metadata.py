from rest_framework import viewsets

from drips.api.filters import DRIPSMetadataFilter
from drips.api.serializers.metadata import DRIPSMetadataSerializer
from drips.api.views.base import GenericAbstractViewSetMixin
from drips.apps.report_metadata.models import DRIPSMetadata


class DRIPSMetadataViewSet(GenericAbstractViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = DRIPSMetadata.objects.all()
    serializer_class = DRIPSMetadataSerializer
    filterset_class = DRIPSMetadataFilter
    search_fields = ('description', 'code')
