import os
import tempfile

import pytest
from rest_framework.test import APIClient

from .factories import (
    BusinessAreaFactory,
    UserFactory,
)


def pytest_configure(config):
    # enable this to remove deprecations
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = "1"
    os.environ['STATIC_ROOT'] = tempfile.gettempdir()


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'notifications.json')


@pytest.fixture()
def client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture()
def user(request, db):
    return UserFactory()


@pytest.fixture()
def logged_user(client, user):
    client.force_authenticate(user)
    return user


@pytest.fixture()
def business_area():
    return BusinessAreaFactory()
