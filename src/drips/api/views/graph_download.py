from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from sharepoint_rest_api import config
from sharepoint_rest_api.graph_client import GraphClient, GraphClientError


class GraphFileDownloadViewSet(viewsets.ViewSet):
    """ViewSet that downloads files via the Microsoft Graph API.

    Accepts ``drive_id`` + ``item_id`` as query parameters to locate
    the file in the target SharePoint site.
    """

    lookup_field = "filename"
    lookup_value_regex = "[^/]+"

    @cached_property
    def client(self):
        try:
            return GraphClient(
                url=f"{config.SHAREPOINT_TENANT}/{config.SHAREPOINT_SITE_TYPE}/{config.SHAREPOINT_SITE}",
                relative_url=f"{config.SHAREPOINT_SITE_TYPE}/{config.SHAREPOINT_SITE}",
                folder="Documents",
            )
        except GraphClientError:
            raise PermissionDenied

    @action(detail=True, methods=["get"])
    def download(self, request, *args, **kwargs):
        filename = kwargs.get("filename")
        folder = kwargs.get("folder", "")
        site_id = request.query_params.get("site_id")
        drive_id = request.query_params.get("drive_id")
        item_id = request.query_params.get("item_id")
        try:
            if drive_id and item_id:
                graph_response = self.client.download_item(drive_id, item_id)
            else:
                if not site_id:
                    return HttpResponseBadRequest("site_id or drive_id+item_id query parameter is required")
                drive_id = self.client.get_drive_id_by_name(folder, site_id=site_id)
                if drive_id:
                    file_path = filename
                else:
                    file_path = f"{folder}/{filename}" if folder else filename
                graph_response = self.client.download_file(file_path, drive_id=drive_id, site_id=site_id)
            django_response = HttpResponse(
                content=graph_response.content,
                status=graph_response.status_code,
                content_type=graph_response.headers.get("Content-Type", "application/octet-stream"),
            )
            django_response["Content-Disposition"] = "attachment; filename=%s" % filename
            return django_response
        except GraphClientError as e:
            return HttpResponseBadRequest(str(e))
