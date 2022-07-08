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


class AutocompleteMetadata(TimeStampedModel):
    BAP = 'bap'
    IP = 'ip'
    AUTOCHOICES = (
        (BAP, 'BAP Document No'),
        (IP, 'IP No'),
    )

    category = models.CharField(choices=AUTOCHOICES, verbose_name=_("Category"), max_length=128)
    code = models.CharField(verbose_name=_("Code"), max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Autocomplete Metadata'
        verbose_name_plural = 'Autocomplete Metadata'

    def __str__(self):
        return f'{self.code} ({self.category})'


class BAPAutocompleteMetadataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category=AutocompleteMetadata.BAP)


class BAPAutocompleteMetadata(AutocompleteMetadata):
    objects = BAPAutocompleteMetadataManager()

    class Meta(AutocompleteMetadata.Meta):
        verbose_name = _('BAP Autocomplete Metadata')
        verbose_name_plural = _('BAP Autocomplete Metadata')
        proxy = True


class IPAutocompleteMetadataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category=AutocompleteMetadata.IP)


class IPAutocompleteMetadata(AutocompleteMetadata):
    objects = IPAutocompleteMetadataManager()

    class Meta(AutocompleteMetadata.Meta):
        verbose_name = _('IP Autocomplete Metadata')
        verbose_name_plural = _('IP Autocomplete Metadata')
        proxy = True
