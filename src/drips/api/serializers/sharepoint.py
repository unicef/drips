from datetime import datetime

from django.conf import settings

from dateutil.parser import parse
from rest_framework import serializers
from rest_framework.reverse import reverse
from sharepoint_rest_api.serializers.fields import CapitalizeSearchSharePointField

from drips.api.serializers.fields import DRIPSSearchSharePointField
from drips.api.serializers.utils import getvalue


class DRIPSSharePointSearchSerializer(serializers.Serializer):
    title = CapitalizeSearchSharePointField()
    author = CapitalizeSearchSharePointField()
    path = CapitalizeSearchSharePointField()

    created = DRIPSSearchSharePointField()
    modified = DRIPSSearchSharePointField()
    business_area = DRIPSSearchSharePointField()
    ip_type = DRIPSSearchSharePointField()
    implementing_partner_name = DRIPSSearchSharePointField()
    cso_type = DRIPSSearchSharePointField()
    responsible_office = DRIPSSearchSharePointField()
    partner_risk_rating = DRIPSSearchSharePointField()
    implementing_partner_code = DRIPSSearchSharePointField()
    fund_reservation_no = DRIPSSearchSharePointField()
    funds_commitment_no = DRIPSSearchSharePointField()

    b_a_p_document_no = DRIPSSearchSharePointField()
    b_a_p_document_type = DRIPSSearchSharePointField()
    program_document_description = DRIPSSearchSharePointField()
    attachment_type = DRIPSSearchSharePointField()
    face_form_no = DRIPSSearchSharePointField()
    face_form_type = DRIPSSearchSharePointField()
    f_a_c_e_form_description = DRIPSSearchSharePointField()
    f_a_c_e_form_date = DRIPSSearchSharePointField()
    responsible_person = DRIPSSearchSharePointField()
    ho_o_approval = DRIPSSearchSharePointField()

    h_a_c_t_transaction_no = DRIPSSearchSharePointField()
    documentuploaded_app = DRIPSSearchSharePointField()
    uploaded_by = DRIPSSearchSharePointField()

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
