from django.http import HttpResponseBadRequest
from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework.response import Response
from sharepoint_rest_api.graph_client import GraphClient, GraphClientError
from sharepoint_rest_api.utils import to_camel

from drips.api.serializers.fields import DRIPSSearchSharePointField
from drips.api.serializers.sharepoint import DRIPSSharePointSearchSerializer
from drips.apps.report_metadata.models import SourceId
from sharepoint_rest_api.views.base import SearchResponseMixin


class DRIPSSharepointSearchViewSet(SearchResponseMixin, viewsets.GenericViewSet):
    serializer_class = DRIPSSharePointSearchSerializer
    filter_backends = []

    @cached_property
    def client(self):
        return GraphClient()

    def _apply_source_id_filters(self, qp):
        source_id = qp.get("source_id")
        if not source_id:
            return
        try:
            source_obj = SourceId.objects.get(source_id=source_id)
            default_filters = source_obj.default_filters or {}
        except SourceId.DoesNotExist:
            default_filters = {}
        for key, value in default_filters.get("filters", {}).items():
            if key not in qp:
                qp[key] = value
        search_kql = default_filters.get("search_kql", "")
        if search_kql:
            existing_search = qp.get("search", "")
            if existing_search:
                qp["search"] = f"({search_kql}) AND ({existing_search})"
            else:
                qp["search"] = search_kql
        exclude_paths = default_filters.get("exclude_paths", [])
        if exclude_paths:
            path_exclusions = " ".join(f'-Path:"{p}"' for p in exclude_paths)
            qp["search"] = f"{path_exclusions} {qp.get('search', '')}".strip()

    def get_filters(self, kwargs):
        new_kwargs = {}
        drp_fields = [
            key
            for key, value in self.serializer_class._declared_fields.items()
            if isinstance(value, DRIPSSearchSharePointField)
        ]

        for key, value in kwargs.items():
            key_splits = key.split("__")
            filter_name = key_splits[0]
            filter_type = key_splits[-1] if len(key_splits) > 1 else None
            if filter_name in drp_fields:
                new_key = "DRIPS" + to_camel(filter_name)
                if filter_type:
                    new_key = f"{new_key}__{filter_type}"
                new_kwargs[new_key] = value
            else:
                new_kwargs[key] = value

        return new_kwargs

    def get_queryset(self):
        qp = self.request.query_params.dict()
        self._apply_source_id_filters(qp)
        search = qp.pop("search", None)
        page = int(qp.pop("page", 1))
        filters = self.get_filters(qp)
        items, self.total_rows = self.client.search(
            search=search,
            filters=filters,
            page=page,
        )
        return items

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
        except GraphClientError as e:
            return HttpResponseBadRequest(str(e))
        return self._build_paginated_response(request, response)
