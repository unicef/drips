import os
from io import StringIO
from unittest import mock

from django.core.management import call_command

import pytest


@pytest.mark.django_db
class TestInitSetupCommand:
    @mock.patch("drips.apps.core.management.commands.init_setup.call_command")
    def test_collectstatic_option(self, mock_django_call):
        call_command("init_setup", collectstatic=True, verbosity=0)
        mock_django_call.assert_any_call("collectstatic", verbosity=-1, interactive=False)

    @mock.patch("drips.apps.core.management.commands.init_setup.call_command")
    def test_migrate_option(self, mock_django_call):
        call_command("init_setup", migrate=True, verbosity=0)
        mock_django_call.assert_any_call("migrate", verbosity=-1)

    @mock.patch.dict(os.environ, {"USER": "admin"})
    @mock.patch("drips.apps.core.management.commands.init_setup.settings")
    def test_users_option_debug(self, mock_settings):
        mock_settings.DEBUG = True
        call_command("init_setup", users=True, verbosity=0)
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.get(username="admin")
        assert user.is_superuser
        assert user.is_staff

    @mock.patch("drips.apps.core.management.commands.init_setup.call_command")
    @mock.patch("drips.apps.core.management.commands.init_setup.sync_business_area")
    def test_metadata_option(self, mock_sync, mock_django_call):
        call_command("init_setup", metadata=True, verbosity=0)
        mock_sync.assert_called_once()
        mock_django_call.assert_any_call("loaddata", "metadata.json")
        mock_django_call.assert_any_call("loaddata", "cost_centers.json")

    @mock.patch("drips.apps.core.management.commands.init_setup.call_command")
    @mock.patch("drips.apps.core.management.commands.init_setup.sync_business_area")
    @mock.patch("drips.apps.core.management.commands.init_setup.settings")
    def test_all_option(self, mock_settings, mock_sync, mock_django_call):
        mock_settings.DEBUG = True
        call_command("init_setup", all=True, verbosity=0)
        mock_django_call.assert_any_call("collectstatic", verbosity=-1, interactive=False)
        mock_django_call.assert_any_call("migrate", verbosity=-1)

    @mock.patch("drips.apps.core.management.commands.init_setup.call_command")
    @mock.patch("drips.apps.core.management.commands.init_setup.sync_business_area")
    def test_metadata_handles_exception(self, mock_sync, mock_django_call):
        mock_sync.side_effect = Exception("sync error")
        stdout = StringIO()
        call_command("init_setup", metadata=True, verbosity=0, stdout=stdout)
        output = stdout.getvalue()
        assert "Error when loading metadata" in output
