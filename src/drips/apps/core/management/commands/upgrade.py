import os
import secrets
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.migrations.exceptions import InconsistentMigrationHistory

from unicef_realm.tasks import sync_business_area


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", action="store_true", dest="all", default=False, help="select all options but `demo`"
        )

        parser.add_argument("--collectstatic", action="store_true", dest="collectstatic", default=False, help="")

        parser.add_argument("--users", action="store_true", dest="users", default=False, help="")

        parser.add_argument("--metadata", action="store_true", dest="metadata", default=False, help="")

        parser.add_argument(
            "--migrate",
            action="store_true",
            dest="migrate",
            default=False,
            help="select all production deployment options",
        )

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        migrate = options["migrate"]
        _all = options["all"]
        user_model = get_user_model()
        if options["collectstatic"] or _all:
            self.stdout.write("Run collectstatic")
            call_command("collectstatic", verbosity=verbosity - 1, interactive=False)

        if migrate or _all:
            self.stdout.write("Run migrations")
            try:
                call_command("migrate", verbosity=verbosity - 1)
            except InconsistentMigrationHistory:
                self.stdout.write(
                    "Migration history is inconsistent (admin applied before core). "
                    "Faking core.0001_initial to resolve..."
                )
                call_command("migrate", "core", "0001_initial", fake=True, verbosity=verbosity - 1)
                call_command("migrate", verbosity=verbosity - 1)

        if options["users"] or _all:
            if settings.DEBUG:
                pwd = "123"  # noqa: S105
                admin = os.environ.get("USER", "admin")
            else:
                random_pwd = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
                pwd = os.environ.get("ADMIN_PASSWORD", random_pwd)
                admin = os.environ.get("ADMIN_USERNAME", "admin")

            _, created = user_model.objects.get_or_create(
                username=admin, defaults={"is_superuser": True, "is_staff": True, "password": make_password(pwd)}
            )

            if created:  # pragma: no cover
                self.stdout.write(f"Created superuser `{admin}` with password `{pwd}`")
            else:  # pragma: no cover
                self.stdout.write(f"Superuser `{admin}` already exists`.")

        try:
            if options["metadata"] or _all:
                sync_business_area()
                call_command("loaddata", "metadata.json")
                call_command("loaddata", "cost_centers.json")
        except Exception as e:  # noqa: BLE001
            self.stdout.write(f"Error when loading metadata: {str(e)}`")
