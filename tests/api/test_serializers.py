from datetime import datetime, timedelta

import pytest

from drips.api.serializers.fields import DRIPSSearchMultiSharePointField, DRIPSSearchSharePointField
from drips.api.serializers.sharepoint import DRIPSSharePointSearchSerializer
from drips.api.serializers.userrole import UserSerializer


class TestDRIPSSearchSharePointField:
    def test_get_attribute_returns_field_with_prefix(self):
        field = DRIPSSearchSharePointField(source="business_area")
        instance = {"DRIPSBusinessArea": "123"}
        result = field.get_attribute(instance)
        assert result == "123"

    def test_get_attribute_returns_na_for_missing(self):
        field = DRIPSSearchSharePointField(source="business_area")
        instance = {}
        result = field.get_attribute(instance)
        assert result == "N/A"

    def test_get_attribute_transform_source(self):
        field = DRIPSSearchSharePointField(source="ip_type")
        instance = {"DRIPSIpType": "programme"}
        result = field.get_attribute(instance)
        assert result == "programme"


class TestDRIPSSearchMultiSharePointField:
    def test_get_attribute_splits_semicolon(self):
        field = DRIPSSearchMultiSharePointField(source="cso_type")
        instance = {"DRIPSCsoType": "gov;ngo;un"}
        result = field.get_attribute(instance)
        assert result == ["gov", "ngo", "un"]

    def test_get_attribute_returns_single_value_list_for_missing(self):
        field = DRIPSSearchMultiSharePointField(source="cso_type")
        instance = {}
        result = field.get_attribute(instance)
        assert result == ["N/A"]

    def test_get_attribute_splits_empty_string(self):
        field = DRIPSSearchMultiSharePointField(source="cso_type")
        instance = {"DRIPSCsoType": ""}
        result = field.get_attribute(instance)
        assert result == []


class TestDRIPSSharePointSearchSerializer:
    def test_get_is_new_returns_true_for_recent(self):
        recent = (datetime.now() - timedelta(hours=12)).isoformat()
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.get_is_new({"DRIPSModified": recent})
        assert result is True

    def test_get_is_new_returns_false_for_old(self):
        old = (datetime.now() - timedelta(days=10)).isoformat()
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.get_is_new({"DRIPSModified": old})
        assert result is False

    def test_get_is_new_returns_none_for_missing(self):
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.get_is_new({})
        assert result is None

    def test_get_is_new_returns_false_for_invalid_date(self):
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.get_is_new({"DRIPSModified": "not-a-date"})
        assert result is False

    @pytest.mark.django_db
    def test_get_download_url_returns_url(self):
        serializer = DRIPSSharePointSearchSerializer()
        obj = {
            "Path": "https://unicef.sharepoint.com/sites/DFAM-DRIPS/2026_07_DRIPS/filename.pdf",
            "DriveId": "b!abc123",
            "DocId": "01ABCDEF",
        }
        result = serializer.get_download_url(obj)
        assert result is not None
        assert "filename.pdf" in result
        assert "2026_07_DRIPS" in result
        assert "drive_id=b!abc123" in result
        assert "item_id=01ABCDEF" in result

    @pytest.mark.django_db
    def test_get_download_url_returns_none_for_exception(self):
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.get_download_url({})
        assert result is None

    def test_serializer_output(self):
        data = {
            "Title": "doc.pdf",
            "Path": "https://sharepoint.com/site/dir/doc.pdf",
            "DRIPSModified": (datetime.now() - timedelta(hours=12)).isoformat(),
            "DRIPSBusinessArea": "123",
            "Author": "John",
        }
        serializer = DRIPSSharePointSearchSerializer()
        result = serializer.to_representation(data)
        assert result["title"] == "doc.pdf"
        assert result["author"] == "John"
        assert result["business_area"] == "123"


class TestUserSerializer:
    def test_validate_email_rejects_uppercase(self):
        from rest_framework import serializers

        serializer = UserSerializer()
        with pytest.raises(serializers.ValidationError):
            serializer.validate_email("Test@Example.com")

    def test_validate_email_accepts_lowercase(self):
        serializer = UserSerializer()
        result = serializer.validate_email("test@example.com")
        assert result == "test@example.com"


@pytest.mark.django_db
class TestModelStr:
    def test_cost_center_str(self):
        from drips.apps.cost_centers.models import CostCenter

        cc = CostCenter(code="CC001", description="Test Center")
        assert str(cc) == "CC001 -Test Center"

    def test_drips_metadata_str(self):
        from drips.apps.report_metadata.models import DRIPSMetadata

        md = DRIPSMetadata(category="type", code="T1", description="Test Metadata")
        assert str(md) == "type | Test Metadata"

    def test_autocomplete_metadata_str(self):
        from drips.apps.report_metadata.models import AutocompleteMetadata

        am = AutocompleteMetadata(category="ip", code="IP001")
        assert str(am) == "IP001 (ip)"

    def test_drips_metadata_create_code(self):
        from drips.apps.report_metadata.models import DRIPSMetadata

        result = DRIPSMetadata.create_code("Test Description")
        assert result == "test_description"

    def test_drips_metadata_save_generates_code(self):
        from drips.apps.report_metadata.models import DRIPSMetadata

        md = DRIPSMetadata(category="type", description="Test Description")
        md.save()
        assert md.code == "test_description"

    def test_drips_metadata_save_keeps_existing_code(self):
        from drips.apps.report_metadata.models import DRIPSMetadata

        md = DRIPSMetadata(category="type", code="EXISTING", description="Test")
        md.save()
        assert md.code == "EXISTING"
