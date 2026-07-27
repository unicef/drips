from datetime import datetime
from urllib.parse import unquote, urlparse

from django.conf import settings

from dateutil.parser import parse
from rest_framework import serializers
from rest_framework.reverse import reverse
from sharepoint_rest_api import config as sp_config
from sharepoint_rest_api.serializers.fields import CapitalizeSearchSharePointField

from drips.api.serializers.fields import DRIPSSearchSharePointField


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

    b_a_p_document_type = DRIPSSearchSharePointField()
    program_document_no = DRIPSSearchSharePointField()
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
        modified = obj.get("DRIPSModified")

        if modified:
            try:
                day_difference = (datetime.now() - parse(modified, ignoretz=True)).days
                return day_difference <= 3
            except TypeError, ValueError:
                return False
        return None

    @staticmethod
    def _extract_site_relative_path(path):
        """Extract the site-relative path from a SharePoint webUrl."""
        parsed = urlparse(path)
        url_path = unquote(parsed.path) if parsed.scheme else unquote(path)
        url_path = url_path.lstrip("/")
        site_prefix = f"{sp_config.SHAREPOINT_SITE_TYPE}/{sp_config.SHAREPOINT_SITE}/"
        if url_path.startswith(site_prefix):
            return url_path[len(site_prefix) :]
        segments = url_path.split("/")
        if len(segments) >= 3 and segments[0] == sp_config.SHAREPOINT_SITE_TYPE:
            return "/".join(segments[2:])
        return "/".join(segments[1:]) if len(segments) > 1 else None

    def get_download_url(self, obj):
        try:
            path = obj.get("Path")
            if not path:
                return None
            relative_path = self._extract_site_relative_path(path)
            if not relative_path:
                return None
            parts = relative_path.rsplit("/", 1)
            if len(parts) != 2:
                return None
            folder, filename = parts
            drive_id = obj.get("DriveId", "")
            item_id = obj.get("DocId", "")
            if not (drive_id and item_id):
                return None
            params = f"drive_id={drive_id}&item_id={item_id}"
            relative_url = reverse(
                "api:sharepoint-graph-files-download",
                kwargs={"folder": folder, "filename": filename},
            )
            return f"{settings.HOST}{relative_url}?{params}"
        except Exception:  # noqa: BLE001
            return None
