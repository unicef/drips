from unittest import mock

import pytest

from drips.apps.report_metadata.tasks import (
    load_autometadata,
    load_bap_metadata,
    load_ip_metadata,
    load_responsible_person_metadata,
    load_uploaded_by_metadata,
)


@pytest.mark.django_db
class TestLoadAutometadata:
    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_load_autometadata_creates_records(self, mock_read_items):
        mock_read_items.return_value = [
            {"fields": {"Title": "item1"}},
            {"fields": {"Title": "item2"}},
            {"fields": {"Title": "item1"}},
        ]
        load_autometadata(folder="Test Folder", category="ip")
        from drips.apps.report_metadata.models import AutocompleteMetadata

        assert AutocompleteMetadata.objects.count() == 2
        assert AutocompleteMetadata.objects.filter(code="item1").exists()
        assert AutocompleteMetadata.objects.filter(code="item2").exists()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_load_autometadata_skips_empty_title(self, mock_read_items):
        mock_read_items.return_value = [
            {"fields": {"Title": ""}},
            {"fields": {}},
            {"fields": {"Title": "valid"}},
        ]
        load_autometadata(folder="Test Folder", category="ip")
        from drips.apps.report_metadata.models import AutocompleteMetadata

        assert AutocompleteMetadata.objects.count() == 1

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_load_autometadata_empty_list(self, mock_read_items):
        mock_read_items.return_value = []
        load_autometadata(folder="Empty Folder", category="ip")
        from drips.apps.report_metadata.models import AutocompleteMetadata

        assert AutocompleteMetadata.objects.count() == 0


@pytest.mark.django_db
class TestConvenienceTasks:
    @mock.patch("drips.apps.report_metadata.tasks.load_autometadata")
    def test_load_ip_metadata(self, mock_load):
        load_ip_metadata()
        mock_load.assert_called_once_with(folder="IP No", category="ip")

    @mock.patch("drips.apps.report_metadata.tasks.load_autometadata")
    def test_load_bap_metadata(self, mock_load):
        load_bap_metadata()
        mock_load.assert_called_once_with(folder="BAP Document No", category="bap")

    @mock.patch("drips.apps.report_metadata.tasks.load_autometadata")
    def test_load_responsible_person_metadata(self, mock_load):
        load_responsible_person_metadata()
        mock_load.assert_called_once_with(folder="Responsible Person", category="responsbile_person")

    @mock.patch("drips.apps.report_metadata.tasks.load_autometadata")
    def test_load_uploaded_by_metadata(self, mock_load):
        load_uploaded_by_metadata()
        mock_load.assert_called_once_with(folder="Uploaded By", category="uploaded_by")
