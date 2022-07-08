from rest_framework import viewsets

from drips.api.filters import AutocompleteMetadataFilter, DRIPSMetadataFilter
from drips.api.serializers.metadata import AutocompleteMetadataSerializer, DRIPSMetadataSerializer
from drips.api.views.base import GenericAbstractViewSetMixin
from drips.apps.report_metadata.models import BAPAutocompleteMetadata, DRIPSMetadata, IPAutocompleteMetadata


class DRIPSMetadataViewSet(GenericAbstractViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = DRIPSMetadata.objects.all()
    serializer_class = DRIPSMetadataSerializer
    filterset_class = DRIPSMetadataFilter
    search_fields = ('description', 'code')


class BAPAutocompleteMetadataViewSet(GenericAbstractViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BAPAutocompleteMetadata.objects.all()
    serializer_class = AutocompleteMetadataSerializer
    filterset_class = AutocompleteMetadataFilter
    search_fields = ('category', 'code')


class IPAutocompleteMetadataViewSet(GenericAbstractViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = IPAutocompleteMetadata.objects.all()
    serializer_class = AutocompleteMetadataSerializer
    filterset_class = AutocompleteMetadataFilter
    search_fields = ('category', 'code')
