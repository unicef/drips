from rest_framework import serializers

from drips.apps.cost_centers.models import CostCenter


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('business_area', 'code', 'description')
