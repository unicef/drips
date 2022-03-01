from django.db import models
from django.utils.translation import gettext as _

from model_utils.models import TimeStampedModel


class DRIPSMetadata(TimeStampedModel):

    category = models.CharField(verbose_name=_("Category"), max_length=128)
    code = models.CharField(verbose_name=_("Code"), max_length=128, null=True, blank=True)
    description = models.CharField(verbose_name=_("Description"), max_length=128)

    class Meta:
        verbose_name = 'Metadata'
        verbose_name_plural = 'Metadata'

    def __str__(self):
        return f'{self.category} | {self.description}'

    @staticmethod
    def create_code(description):
        return description.lower().replace(' ', '_')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.create_code(self.description)
        super().save(*args, **kwargs)
