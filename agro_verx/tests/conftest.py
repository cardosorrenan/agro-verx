import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from agro_verx.producer.models import ProducerModel

from .factories import generate_producer_data


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'producer_producer')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def producer_data():
    return generate_producer_data()


@pytest.fixture
def create_producer():
    def make_producer(**kwargs):
        return ProducerModel.objects.create(**kwargs)

    return make_producer
