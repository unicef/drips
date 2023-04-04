from django.urls import reverse

import pytest
from drf_api_checker.pytest import contract, frozenfixture

from tests.api_checker import LastModifiedRecorder
from tests.factories import BusinessAreaFactory, UserFactory


@frozenfixture()
def user(request, db):
    return UserFactory()


@frozenfixture()
def business_area(request, db):
    return BusinessAreaFactory()


@contract(recorder_class=LastModifiedRecorder)
def test_api_user_list(request, django_app, user):
    return reverse("api:user-list")


@contract(recorder_class=LastModifiedRecorder)
def test_api_user_profile(request, django_app, logged_user):
    return reverse("api:user-my-profile")


@pytest.mark.django_db
@contract(LastModifiedRecorder)
def test_api_business_area_list(request, django_app, business_area):
    return reverse("api:businessarea-list")
