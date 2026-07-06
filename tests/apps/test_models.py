import pytest

from drips.apps.report_metadata.models import SourceId


@pytest.mark.django_db
class TestSourceIdModel:
    def test_str(self):
        obj = SourceId.objects.create(name="Test", source_id="S123")
        assert str(obj) == "Test | S123"
