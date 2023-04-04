from django.db.models import signals

import factory
import unicef_security
from factory import SubFactory
from unicef_realm.models import BusinessArea, Region


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = unicef_security.models.User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: "user%03d" % n)

    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")

    email = factory.Sequence(lambda n: "m%03d@mailinator.com" % n)
    password = "password"
    is_superuser = False
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        from ..perms import user_grant_permissions

        permissions = kwargs.pop("permissions", [])

        password = kwargs.pop("password")
        user = super()._prepare(cls, create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        user_grant_permissions(user, permissions).start()
        return user


class AdminFactory(UserFactory):
    is_superuser = True


class AnonUserFactory(UserFactory):
    username = "anonymous"


class RegionFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = Region
        django_get_or_create = ("name",)


class BusinessAreaFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    region = SubFactory(RegionFactory)

    class Meta:
        model = BusinessArea
        django_get_or_create = ("code",)
