from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters
from unicef_realm.models import BusinessArea

from drips.apps.cost_centers.models import CostCenter
from drips.apps.report_metadata.models import AutocompleteMetadata, DRIPSMetadata


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


class AutocompleteMetadataFilter(filters.FilterSet):
    class Meta:
        model = AutocompleteMetadata
        fields = {
            'code': ['exact', 'startswith'],
            'category': ['exact', 'startswith'],
        }


class CostCenterFilter(filters.FilterSet):
    class Meta:
        model = CostCenter
        fields = {
            'code': ['exact', 'in', 'icontains'],
            'description': ['exact', 'in', 'icontains'],
        }
