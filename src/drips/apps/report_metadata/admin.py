from django.contrib import admin

from .models import DRIPSMetadata


@admin.register(DRIPSMetadata)
class DRIPSMetadata(admin.ModelAdmin):
    search_fields = ('description', 'code')
    list_display = ('category', 'description')
    list_filter = ('category', )
