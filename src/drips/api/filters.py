from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters
from unicef_security.models import BusinessArea

from drips.apps.report_metadata.models import DRIPSMetadata


class UserFilter(filters.FilterSet):

    class Meta:
        model = get_user_model()
        fields = {
            'username': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
        }


class BusinessAreaFilter(filters.FilterSet):

    class Meta:
        model = BusinessArea
        fields = {
            'region': ['exact', 'in'],
            'country': ['exact', 'in'],
        }


class DRIPSMetadataFilter(filters.FilterSet):

    class Meta:
        model = DRIPSMetadata
        fields = {
            'category': ['exact', 'in'],
        }
