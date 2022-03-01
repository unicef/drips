from datetime import datetime

from django.conf import settings

from dateutil.parser import parse
from rest_framework import serializers
from rest_framework.reverse import reverse
from sharepoint_rest_api.serializers.fields import (
    CapitalizeSearchSharePointField,
)

from drips.api.serializers.fields import DRIPSSearchMultiSharePointField, DRIPSSearchSharePointField
from drips.api.serializers.utils import getvalue


class DRIPSSharePointSearchSerializer(serializers.Serializer):
    title = CapitalizeSearchSharePointField()
    author = CapitalizeSearchSharePointField()
    path = CapitalizeSearchSharePointField()

    created = DRIPSSearchSharePointField()
    modified = DRIPSSearchSharePointField()
    business_area = DRIPSSearchSharePointField()
    ip_type = DRIPSSearchSharePointField()
    cso_type = DRIPSSearchSharePointField()
    office = DRIPSSearchMultiSharePointField()

    risk_rating = DRIPSSearchSharePointField()
    ip_number = DRIPSSearchSharePointField()
    bap_document_no = DRIPSSearchSharePointField()
    bap_document_type = DRIPSSearchSharePointField()
    document_type = DRIPSSearchSharePointField()
    face_type = DRIPSSearchSharePointField()
    face_no = DRIPSSearchSharePointField()
    programme_officer = DRIPSSearchSharePointField()
    face_date = DRIPSSearchSharePointField()
    head_of_office = DRIPSSearchSharePointField()
    uploading_app = DRIPSSearchSharePointField()

    is_new = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    def get_is_new(self, obj):
        modified = getvalue(obj, 'DRIPSModified')

        if modified:
            try:
                day_difference = (datetime.now() - parse(modified, ignoretz=True)).days
                return day_difference <= 3
            except (TypeError, ValueError):
                return False

    def get_download_url(self, obj):
        try:
            path = getvalue(obj, 'Path')
            directories = path.split('/')
            relative_url = reverse('sharepoint_rest_api:sharepoint-settings-files-download', kwargs={
                'folder': directories[-2],
                'filename': directories[-1]
            })
            return f'{settings.HOST}{relative_url}'
        except BaseException:
            return None
