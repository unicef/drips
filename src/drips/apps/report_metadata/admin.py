import logging

from django.contrib import admin, messages

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin

from .models import (
    BAPAutocompleteMetadata,
    DRIPSMetadata,
    IPAutocompleteMetadata,
    ResponsiblePersonAutocompleteMetadata,
    UploadedByAutocompleteMetadata,
)
from .tasks import load_bap_metadata, load_ip_metadata, load_responsible_person_metadata, load_uploaded_by_metadata

logger = logging.getLogger(__name__)


@admin.register(DRIPSMetadata)
class DRIPSMetadataAdmin(admin.ModelAdmin):
    search_fields = ('description', 'code')
    list_display = ('category', 'description')
    list_filter = ('category', )


@admin.register(BAPAutocompleteMetadata)
class BAPAutocompleteMetadataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )

    @button()
    def sync(self, request):
        try:
            load_bap_metadata()
        except BaseException as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)

    @button()
    def truncate(self, request):
        n = BAPAutocompleteMetadata.objects.count()
        BAPAutocompleteMetadata.objects.all().delete()
        self.message_user(request, str(f'Metadata {n} deleted'), messages.ERROR)


@admin.register(IPAutocompleteMetadata)
class IPAutocompleteMetadataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )

    @button()
    def sync(self, request):
        try:
            load_ip_metadata()
        except BaseException as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)

    @button()
    def truncate(self, request):
        n = IPAutocompleteMetadata.objects.count()
        IPAutocompleteMetadata.objects.all().delete()
        self.message_user(request, str(f'Metadata {n} deleted'), messages.ERROR)


@admin.register(ResponsiblePersonAutocompleteMetadata)
class ResponsiblePersonAutocompleteMetadataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )

    @button()
    def sync(self, request):
        try:
            load_responsible_person_metadata()
        except BaseException as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)

    @button()
    def truncate(self, request):
        n = ResponsiblePersonAutocompleteMetadata.objects.count()
        ResponsiblePersonAutocompleteMetadata.objects.all().delete()
        self.message_user(request, str(f'Metadata {n} deleted'), messages.ERROR)


@admin.register(UploadedByAutocompleteMetadata)
class UploadedByAutocompleteMetadataAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )

    @button()
    def sync(self, request):
        try:
            load_uploaded_by_metadata()
        except BaseException as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)

    @button()
    def truncate(self, request):
        n = UploadedByAutocompleteMetadata.objects.count()
        UploadedByAutocompleteMetadata.objects.all().delete()
        self.message_user(request, str(f'Metadata {n} deleted'), messages.ERROR)
