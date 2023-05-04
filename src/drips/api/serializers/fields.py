from rest_framework import serializers
from sharepoint_rest_api.utils import to_camel


class DRIPSSearchSharePointField(serializers.ReadOnlyField):
    prefix = "DRIPS"

    def get_attribute(self, instance):
        field_name = self.prefix + to_camel(self.source)
        return instance.get(field_name, "N/A")


class DRIPSSearchMultiSharePointField(DRIPSSearchSharePointField):
    def get_attribute(self, instance):
        attrs = super().get_attribute(instance)
        return attrs.split(";") if attrs else []
