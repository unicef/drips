from django.contrib import admin

from .models import CostCenter


@admin.register(CostCenter)
class CostCenterMetadata(admin.ModelAdmin):
    search_fields = ('description', 'code')
    list_display = ('business_area', 'code', 'description')
    list_filter = ('business_area', )
