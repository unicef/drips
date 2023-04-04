from rest_framework import serializers

from drips.apps.report_metadata.models import AutocompleteMetadata, DRIPSMetadata


class DRIPSMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRIPSMetadata
        fields = ("category", "code", "description")


class AutocompleteMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutocompleteMetadata
        fields = ("category", "code")
