from sharepoint_rest_api.utils import to_camel
from sharepoint_rest_api.views.settings_based import SharePointSettingsSearchViewSet

from drips.api.serializers.fields import DRIPSSearchSharePointField
from drips.api.serializers.sharepoint import DRIPSSharePointSearchSerializer


class DRIPSSharepointSearchViewSet(SharePointSettingsSearchViewSet):
    prefix = 'DRIPS'
    serializer_class = DRIPSSharePointSearchSerializer

    def is_public(self):
        """check if the source id is public or restricted to UNICEF users"""
        return True

    def get_selected(self, selected):
        def to_drips(source):
            return self.prefix + to_camel(source)
        selected = super().get_selected(selected)
        return [to_drips(x) for x in selected] + ["Title", "Author", "Path"]

    def get_filters(self, kwargs):
        # we can enforce filters here
        new_kwargs = {
            # 'IsDocument': '1',
        }
        drp_fields = [key for key, value in self.serializer_class._declared_fields.items()
                      if isinstance(value, DRIPSSearchSharePointField)]

        for key, value in kwargs.items():
            key_splits = key.split('__')
            filter_name = key_splits[0]
            filter_type = key_splits[-1] if len(key_splits) > 1 else None
            if filter_name in drp_fields:
                new_key = self.prefix + to_camel(filter_name)
                if filter_type:
                    new_key = f'{new_key}__{filter_type}'
                new_kwargs[new_key] = value
            else:
                new_kwargs[key] = value

        return new_kwargs
