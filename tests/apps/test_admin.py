from unittest import mock

from django.test.client import RequestFactory

import pytest

from drips.apps.report_metadata.admin import (
    BAPAutocompleteMetadataAdmin,
    IPAutocompleteMetadataAdmin,
    ResponsiblePersonAutocompleteMetadataAdmin,
    UploadedByAutocompleteMetadataAdmin,
)
from drips.apps.report_metadata.models import (
    BAPAutocompleteMetadata,
    IPAutocompleteMetadata,
    ResponsiblePersonAutocompleteMetadata,
    UploadedByAutocompleteMetadata,
)


def _make_request():
    request = RequestFactory().get("/")
    request.user = mock.MagicMock()
    request.session = {}
    from django.contrib.messages.storage.fallback import FallbackStorage

    request._messages = FallbackStorage(request)
    return request


@pytest.mark.django_db
class TestAdminSyncButtons:
    def _call_button(self, admin_class, admin_instance, request):
        return admin_class.__dict__["sync"].func(admin_instance, request)

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_bap_sync_button(self, mock_read_items):
        mock_read_items.return_value = []
        admin = BAPAutocompleteMetadataAdmin(BAPAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(BAPAutocompleteMetadataAdmin, admin, request)
        mock_read_items.assert_called_once()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_ip_sync_button(self, mock_read_items):
        mock_read_items.return_value = []
        admin = IPAutocompleteMetadataAdmin(IPAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(IPAutocompleteMetadataAdmin, admin, request)
        mock_read_items.assert_called_once()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_responsible_person_sync_button(self, mock_read_items):
        mock_read_items.return_value = []
        admin = ResponsiblePersonAutocompleteMetadataAdmin(ResponsiblePersonAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(ResponsiblePersonAutocompleteMetadataAdmin, admin, request)
        mock_read_items.assert_called_once()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_uploaded_by_sync_button(self, mock_read_items):
        mock_read_items.return_value = []
        admin = UploadedByAutocompleteMetadataAdmin(UploadedByAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(UploadedByAutocompleteMetadataAdmin, admin, request)
        mock_read_items.assert_called_once()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.read_list_items")
    def test_sync_button_handles_error(self, mock_read_items):
        mock_read_items.side_effect = Exception("sync failed")
        admin = BAPAutocompleteMetadataAdmin(BAPAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(BAPAutocompleteMetadataAdmin, admin, request)
        mock_read_items.assert_called_once()


@pytest.mark.django_db
class TestAdminTruncateButtons:
    def _call_button(self, admin_class, admin_instance, request):
        return admin_class.__dict__["truncate"].func(admin_instance, request)

    def test_bap_truncate_button(self):
        BAPAutocompleteMetadata.objects.create(code="test1", category="bap")
        BAPAutocompleteMetadata.objects.create(code="test2", category="bap")
        admin = BAPAutocompleteMetadataAdmin(BAPAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(BAPAutocompleteMetadataAdmin, admin, request)
        assert BAPAutocompleteMetadata.objects.count() == 0

    def test_ip_truncate_button(self):
        IPAutocompleteMetadata.objects.create(code="test1", category="ip")
        admin = IPAutocompleteMetadataAdmin(IPAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(IPAutocompleteMetadataAdmin, admin, request)
        assert IPAutocompleteMetadata.objects.count() == 0

    def test_responsible_person_truncate_button(self):
        ResponsiblePersonAutocompleteMetadata.objects.create(code="test1", category="responsbile_person")
        admin = ResponsiblePersonAutocompleteMetadataAdmin(ResponsiblePersonAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(ResponsiblePersonAutocompleteMetadataAdmin, admin, request)
        assert ResponsiblePersonAutocompleteMetadata.objects.count() == 0

    def test_uploaded_by_truncate_button(self):
        UploadedByAutocompleteMetadata.objects.create(code="test1", category="uploaded_by")
        admin = UploadedByAutocompleteMetadataAdmin(UploadedByAutocompleteMetadata, mock.MagicMock())
        request = _make_request()
        self._call_button(UploadedByAutocompleteMetadataAdmin, admin, request)
        assert UploadedByAutocompleteMetadata.objects.count() == 0
