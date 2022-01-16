import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def user_factory():
    def factory(**kwargs):
        return baker.make('accounts.User', **kwargs)
    return factory


@pytest.fixture()
def contact_factory():
    def factory(**kwargs):
        return baker.make('accounts.Contact', **kwargs)
    return factory
