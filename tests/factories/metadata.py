import factory

from drips.apps.report_metadata.models import DRIPSMetadata


class DRIPSMetadataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DRIPSMetadata
