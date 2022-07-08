from django.contrib import admin

from .models import BAPAutocompleteMetadata, DRIPSMetadata, IPAutocompleteMetadata


@admin.register(DRIPSMetadata)
class DRIPSMetadataAdmin(admin.ModelAdmin):
    search_fields = ('description', 'code')
    list_display = ('category', 'description')
    list_filter = ('category', )


@admin.register(BAPAutocompleteMetadata)
class BAPAutocompleteMetadataAdmin(admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )


@admin.register(IPAutocompleteMetadata)
class IPAutocompleteMetadata(admin.ModelAdmin):
    search_fields = ('category', )
    list_display = ('code', )
    list_filter = ('category', )
