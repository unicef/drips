from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from unicef_security.models import BusinessArea, User

from drips.api.filters import BusinessAreaFilter, UserFilter
from drips.api.serializers.userrole import BusinessAreaSerializer, UserSerializer
from drips.api.views.base import GenericAbstractViewSetMixin


class UserViewSet(GenericAbstractViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    search_fields = ('user__username', 'group__name')

    @action(detail=False, methods=['get'])
    def my_profile(self, request, *args, **kwargs):
        object = self.request.user
        serializer = UserSerializer(object)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'my_profile':
            return [IsAuthenticated(), ]
        return super().get_permissions()


class BusinessAreaViewSet(GenericAbstractViewSetMixin, viewsets.ModelViewSet):
    queryset = BusinessArea.objects.all()
    serializer_class = BusinessAreaSerializer
    filterset_class = BusinessAreaFilter
    search_fields = ('code', 'name', 'long_name')
