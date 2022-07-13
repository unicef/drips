from rest_framework import serializers

from drips.apps.cost_centers.models import CostCenter


class CostCenterSerializer(serializers.ModelSerializer):
    business_area_code = serializers.ReadOnlyField(source='business_area.code')

    class Meta:
        model = CostCenter
        fields = ('business_area', 'code', 'description', 'business_area_code')
