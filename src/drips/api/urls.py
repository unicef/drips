from django.urls import include, path

from rest_framework import routers

from drips.api.views.config import ConfigAPIView

from .views.metadata import DRIPSMetadataViewSet
from .views.sharepoint import DRIPSSharepointSearchViewSet
from .views.userrole import BusinessAreaViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'business-area', BusinessAreaViewSet)
router.register(r'roles/users', UserViewSet)
router.register(r'metadata', DRIPSMetadataViewSet, basename='metadata')
router.register(r'sharepoint/search', DRIPSSharepointSearchViewSet, basename='sharepoint-search')

urlpatterns = [
    path('config/', view=ConfigAPIView.as_view(http_method_names=['get']), name='config-list'),
    path(r'', include(router.urls)),
]
