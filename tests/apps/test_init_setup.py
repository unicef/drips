import os
from io import StringIO
from unittest import mock

from django.core.management import call_command

import pytest


@pytest.mark.django_db
class TestUpgradeCommand:
    @mock.patch("drips.apps.core.management.commands.upgrade.call_command")
    def test_collectstatic_option(self, mock_django_call):
        call_command("upgrade", collectstatic=True, verbosity=0)
        mock_django_call.assert_any_call("collectstatic", verbosity=-1, interactive=False)

    @mock.patch("drips.apps.core.management.commands.upgrade.call_command")
    def test_migrate_option(self, mock_django_call):
        call_command("upgrade", migrate=True, verbosity=0)
        mock_django_call.assert_any_call("migrate", verbosity=-1)

    @mock.patch.dict(os.environ, {"USER": "admin"})
    @mock.patch("drips.apps.core.management.commands.upgrade.settings")
    def test_users_option_debug(self, mock_settings):
        mock_settings.DEBUG = True
        call_command("upgrade", users=True, verbosity=0)
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.get(username="admin")
        assert user.is_superuser
        assert user.is_staff

    @mock.patch("drips.apps.core.management.commands.upgrade.call_command")
    @mock.patch("drips.apps.core.management.commands.upgrade.sync_business_area")
    def test_metadata_option(self, mock_sync, mock_django_call):
        call_command("upgrade", metadata=True, verbosity=0)
        mock_sync.assert_called_once()
        mock_django_call.assert_any_call("loaddata", "metadata.json")
        mock_django_call.assert_any_call("loaddata", "cost_centers.json")

    @mock.patch("drips.apps.core.management.commands.upgrade.get_user_model")
    @mock.patch.dict(os.environ, {"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "testpass"})
    @mock.patch("drips.apps.core.management.commands.upgrade.settings")
    def test_users_option_no_debug(self, mock_settings, mock_get_user):
        mock_settings.DEBUG = False
        mock_user_model = mock.MagicMock()
        mock_user_model.objects.get_or_create.return_value = (mock.MagicMock(), True)
        mock_get_user.return_value = mock_user_model
        call_command("upgrade", users=True, verbosity=0)
        mock_user_model.objects.get_or_create.assert_called_once_with(
            username="admin",
            defaults=mock.ANY,
        )

    @mock.patch("drips.apps.core.management.commands.upgrade.get_user_model")
    @mock.patch.dict(os.environ, {"ADMIN_USERNAME": "admin"})
    @mock.patch("drips.apps.core.management.commands.upgrade.settings")
    def test_users_option_no_debug_random_password(self, mock_settings, mock_get_user):
        mock_settings.DEBUG = False
        mock_user_model = mock.MagicMock()
        mock_user_model.objects.get_or_create.return_value = (mock.MagicMock(), True)
        mock_get_user.return_value = mock_user_model
        call_command("upgrade", users=True, verbosity=0)
        mock_user_model.objects.get_or_create.assert_called_once_with(
            username="admin",
            defaults=mock.ANY,
        )

    @mock.patch("drips.apps.core.management.commands.upgrade.call_command")
    @mock.patch("drips.apps.core.management.commands.upgrade.sync_business_area")
    @mock.patch("drips.apps.core.management.commands.upgrade.settings")
    def test_all_option(self, mock_settings, mock_sync, mock_django_call):
        mock_settings.DEBUG = True
        call_command("upgrade", all=True, verbosity=0)
        mock_django_call.assert_any_call("collectstatic", verbosity=-1, interactive=False)
        mock_django_call.assert_any_call("migrate", verbosity=-1)

    @mock.patch("drips.apps.core.management.commands.upgrade.call_command")
    @mock.patch("drips.apps.core.management.commands.upgrade.sync_business_area")
    def test_metadata_handles_exception(self, mock_sync, mock_django_call):
        mock_sync.side_effect = Exception("sync error")
        stdout = StringIO()
        call_command("upgrade", metadata=True, verbosity=0, stdout=stdout)
        output = stdout.getvalue()
        assert "Error when loading metadata" in output
