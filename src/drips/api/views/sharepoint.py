from django.http import HttpResponseBadRequest
from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework.response import Response
from sharepoint_rest_api.graph_client import GraphClient, GraphClientError
from sharepoint_rest_api.utils import to_camel

from drips.api.serializers.fields import DRIPSSearchSharePointField
from drips.api.serializers.sharepoint import DRIPSSharePointSearchSerializer
from drips.api.views.properties import PROPERTY_TO_MANAGED
from sharepoint_rest_api.models import SourceId
from sharepoint_rest_api.views.base import SearchResponseMixin


class DRIPSSharepointSearchViewSet(SearchResponseMixin, viewsets.GenericViewSet):
    serializer_class = DRIPSSharePointSearchSerializer
    filter_backends = []

    @cached_property
    def client(self):
        return GraphClient()

    @staticmethod
    def _build_filter_kql(filters):
        clauses = []
        for name, value in filters.items():
            parts = name.split("__")
            prop = parts[0]
            op = parts[-1] if len(parts) > 1 else "eq"
            if op == "not":
                clauses.append(f'-{prop}:"{value}"')
            elif op == "contains":
                clauses.append(f'{prop}:"{value}*"')
            elif op in ("gte", "gt", "lte", "lt"):
                kql_op = {"gte": ">=", "gt": ">", "lte": "<=", "lt": "<"}[op]
                clauses.append(f"{prop}{kql_op}{value}")
            else:
                clauses.append(f'{prop}:"{value}"')
        return " ".join(clauses)

    @staticmethod
    def _get_source_id_default_filters(source_id):
        try:
            source_obj = SourceId.objects.get(source_id=source_id)
            return source_obj.default_filters or {}
        except SourceId.DoesNotExist:
            return {}

    @staticmethod
    def _build_source_search_kql(default_filters):
        parts = []
        for paths, negate in (
            (default_filters.get("include_paths", []), False),
            (default_filters.get("exclude_paths", []), True),
        ):
            if paths:
                prefix = "-" if negate else ""
                parts.extend(f'{prefix}Path:"{p}"' for p in paths)
        kql = default_filters.get("search_kql", "")
        if kql:
            parts.append(kql)
        filters = default_filters.get("filters", {})
        if filters:
            parts.append(DRIPSSharepointSearchViewSet._build_filter_kql(filters))
        return " ".join(parts)

    def _apply_source_id_filters(self, qp):
        source_id = qp.get("source_id")
        if not source_id:
            return
        default_filters = self._get_source_id_default_filters(source_id)
        search_kql = self._build_source_search_kql(default_filters)
        if search_kql:
            existing = qp.get("search", "")
            qp["search"] = f"{search_kql} {existing}".strip() if existing else search_kql
        if "order_by" not in qp:
            qp["order_by"] = default_filters.get("order_by", "modified desc")

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
                camel_name = to_camel(filter_name)
                managed = PROPERTY_TO_MANAGED.get(camel_name)
                new_key = managed or "DRIPS" + camel_name
                if filter_type:
                    new_key = f"{new_key}__{filter_type}"
                new_kwargs[new_key] = value
            else:
                new_kwargs[key] = value

        return new_kwargs

    def get_queryset(self):
        qp = self.request.query_params.dict()
        self._apply_source_id_filters(qp)
        qp.setdefault("order_by", "modified desc")
        search = qp.pop("search", None)
        page = int(qp.pop("page", 1))
        order_by = qp.pop("order_by", None)
        filters = self.get_filters(qp)

        reverse_map = {}
        for name, field in self.serializer_class._declared_fields.items():
            if isinstance(field, DRIPSSearchSharePointField):
                camel_name = to_camel(name)
                managed = PROPERTY_TO_MANAGED.get(camel_name)
                if managed:
                    reverse_map[managed] = "DRIPS" + camel_name

        items, self.total_rows = self.client.search(
            search=search,
            filters=filters,
            page=page,
            searchable_properties=set(PROPERTY_TO_MANAGED.values()),
            reverse_map=reverse_map,
            order_by=order_by,
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
