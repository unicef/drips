from django.urls import include, path

from rest_framework import routers

from drips.api.views.config import ConfigAPIView

from .views.cost_centres import CostCenterViewSet
from .views.metadata import (
    BAPAutocompleteMetadataViewSet,
    DRIPSMetadataViewSet,
    IPAutocompleteMetadataViewSet,
    ResponsiblePersonAutocompleteMetadataViewSet,
    UploadedByAutocompleteMetadataViewSet,
)
from .views.sharepoint import DRIPSSharepointSearchViewSet
from .views.userrole import BusinessAreaViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'business-area', BusinessAreaViewSet)
router.register(r'roles/users', UserViewSet)
router.register(r'metadata', DRIPSMetadataViewSet, basename='metadata')
router.register(r'ip-metadata', IPAutocompleteMetadataViewSet, basename='ip-auto')
router.register(r'bap-metadata', BAPAutocompleteMetadataViewSet, basename='bap-auto')
router.register(r'responsible-person-metadata', ResponsiblePersonAutocompleteMetadataViewSet, basename='rp-auto')
router.register(r'uploaded-by-metadata', UploadedByAutocompleteMetadataViewSet, basename='uploaded-by-auto')
router.register(r'costcenters', CostCenterViewSet, basename='costcenters')
router.register(r'sharepoint/search', DRIPSSharepointSearchViewSet, basename='sharepoint-search')

urlpatterns = [
    path('config/', view=ConfigAPIView.as_view(http_method_names=['get']), name='config-list'),
    path(r'', include(router.urls)),
]
