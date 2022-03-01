from rest_framework import serializers

from drips.apps.report_metadata.models import DRIPSMetadata


class DRIPSMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRIPSMetadata
        fields = ('category', 'code', 'description')
