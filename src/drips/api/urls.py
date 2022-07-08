from django.urls import include, path

from rest_framework import routers

from drips.api.views.config import ConfigAPIView

from .views.cost_centres import CostCenterViewSet
from .views.metadata import BAPAutocompleteMetadataViewSet, DRIPSMetadataViewSet, IPAutocompleteMetadataViewSet
from .views.sharepoint import DRIPSSharepointSearchViewSet
from .views.userrole import BusinessAreaViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'business-area', BusinessAreaViewSet)
router.register(r'roles/users', UserViewSet)
router.register(r'metadata', DRIPSMetadataViewSet, basename='metadata')
router.register(r'ip-metadata', IPAutocompleteMetadataViewSet, basename='ip-auto')
router.register(r'bap-metadata', BAPAutocompleteMetadataViewSet, basename='bap-auto')
router.register(r'costcenter', CostCenterViewSet, basename='costcenter')
router.register(r'sharepoint/search', DRIPSSharepointSearchViewSet, basename='sharepoint-search')

urlpatterns = [
    path('config/', view=ConfigAPIView.as_view(http_method_names=['get']), name='config-list'),
    path(r'', include(router.urls)),
]
