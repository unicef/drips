from django.urls import reverse

from drf_api_checker.pytest import contract, frozenfixture

from tests.api_checker import LastModifiedRecorder
from tests.factories import DRIPSMetadataFactory


@frozenfixture()
def metadata(
    request,
    db,
):
    return DRIPSMetadataFactory()


@contract(recorder_class=LastModifiedRecorder)
def test_metadata_list(request, django_app, logged_user, metadata):
    return reverse("api:metadata-list")
