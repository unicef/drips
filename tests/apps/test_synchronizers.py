from datetime import datetime


from drips.apps.report_metadata.synchronizers import get_date


class TestGetDate:
    def test_returns_datetime_for_valid_string(self):
        result = get_date("15-Jan-24")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_returns_none_for_empty_string(self):
        assert get_date("") is None

    def test_returns_none_for_none(self):
        assert get_date(None) is None

    def test_returns_datetime_with_default_format(self):
        result = get_date("01-Feb-24")
        assert result.month == 2
        assert result.day == 1
