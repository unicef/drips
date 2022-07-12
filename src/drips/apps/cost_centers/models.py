from django.db import models
from django.utils.translation import gettext as _

from model_utils.models import TimeStampedModel
from unicef_realm.models import BusinessArea


class CostCenter(TimeStampedModel):

    business_area = models.ForeignKey(BusinessArea, on_delete=models.CASCADE)
    code = models.CharField(verbose_name=_("Code"), max_length=10)
    description = models.CharField(verbose_name=_("Description"), max_length=128)

    class Meta:
        verbose_name = 'CostCentre'
        verbose_name_plural = 'CostCentres'

    def __str__(self):
        return f'{self.code} -{self.description}'
