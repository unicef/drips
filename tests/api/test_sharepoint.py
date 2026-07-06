from unittest import mock

from django.urls import reverse

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestSharepointSearchViewSet:
    def test_search_requires_auth(self, client):
        url = reverse("api:sharepoint-search-list")
        anon_client = __import__("rest_framework").test.APIClient()
        response = anon_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_source_id(self, mock_search, client):
        from drips.apps.report_metadata.models import SourceId

        SourceId.objects.create(source_id="test-source", name="Test Source")
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"source_id": "test-source"})
        assert response.status_code == status.HTTP_200_OK

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_source_id_default_filters(self, mock_search, client):
        from drips.apps.report_metadata.models import SourceId

        SourceId.objects.create(
            source_id="test-source",
            name="Test Source",
            default_filters={
                "filters": {"business_area": "456", "ip_type": "programme"},
                "search_kql": "test_kql",
                "exclude_paths": ["/path1"],
            },
        )
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"source_id": "test-source", "ip_type": "existing"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["filters"]["DRIPSBusinessArea"] == "456"
        assert kwargs["filters"]["DRIPSIpType"] == "existing"
        assert "test_kql" in kwargs["search"]
        assert '-Path:"/path1"' in kwargs["search"]

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_source_id_default_filters_and_existing_search(self, mock_search, client):
        from drips.apps.report_metadata.models import SourceId

        SourceId.objects.create(
            source_id="test-source",
            name="Test Source",
            default_filters={
                "search_kql": "test_kql",
            },
        )
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"source_id": "test-source", "search": "my query"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert "(test_kql) AND (my query)" in kwargs["search"]

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_source_id_not_found(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"source_id": "nonexistent"})
        assert response.status_code == status.HTTP_200_OK

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_non_drips_field(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"foobar": "baz"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["filters"]["foobar"] == "baz"

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_returns_paginated_results(self, mock_search, client):
        mock_search.return_value = (
            [
                {
                    "Title": "doc1.pdf",
                    "Path": "https://sharepoint.com/site/dir/doc1.pdf",
                    "DRIPSModified": "2024-01-15T10:00:00Z",
                    "DRIPSBusinessArea": "123",
                    "Author": "John Doe",
                },
                {
                    "Title": "doc2.pdf",
                    "Path": "https://sharepoint.com/site/dir/doc2.pdf",
                    "DRIPSModified": "2024-01-10T10:00:00Z",
                    "DRIPSBusinessArea": "456",
                    "Author": "Jane Doe",
                },
            ],
            2,
        )
        url = reverse("api:sharepoint-search-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_rows"] == 2
        assert len(data["items"]) == 2
        assert data["items"][0]["title"] == "doc1.pdf"
        assert data["items"][0]["author"] == "John Doe"
        assert data["items"][1]["title"] == "doc2.pdf"

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_filters(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"business_area": "123", "ip_type": "programme"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["filters"]["DRIPSBusinessArea"] == "123"
        assert kwargs["filters"]["DRIPSIpType"] == "programme"

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_non_drips_filters(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"search": "test query"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["search"] == "test query"

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_with_filter_operator(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"business_area__not": "999"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["filters"]["DRIPSBusinessArea__not"] == "999"

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_returns_is_new_true(self, mock_search, client):
        from datetime import datetime, timedelta

        recent = (datetime.now() - timedelta(hours=12)).isoformat()
        mock_search.return_value = (
            [
                {
                    "Title": "recent.pdf",
                    "Path": "https://sharepoint.com/site/dir/recent.pdf",
                    "DRIPSModified": recent,
                    "Author": "John",
                },
            ],
            1,
        )
        url = reverse("api:sharepoint-search-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"][0]["is_new"] is True

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_handles_graph_error(self, mock_search, client):
        from sharepoint_rest_api.graph_client import GraphClientError

        mock_search.side_effect = GraphClientError("API unavailable")
        url = reverse("api:sharepoint-search-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "API unavailable" in response.content.decode()

    @mock.patch("sharepoint_rest_api.graph_client.GraphClient.search")
    def test_search_pagination(self, mock_search, client):
        mock_search.return_value = ([], 0)
        url = reverse("api:sharepoint-search-list")
        response = client.get(url, {"page": "2"})
        assert response.status_code == status.HTTP_200_OK
        _name, args, kwargs = mock_search.mock_calls[0]
        assert kwargs["page"] == 2
