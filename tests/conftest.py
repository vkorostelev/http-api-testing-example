import pytest

from framework.config import SERVICE_URL, USE_MOCK
from framework.payload_generator import PayloadGenerator
from framework.service_api import ServiceAPI


@pytest.fixture(name='payload_generator')
def payload_generator_fixture():
    return PayloadGenerator()


@pytest.fixture(name='service_api')
def service_api_fixture():
    return ServiceAPI(SERVICE_URL, USE_MOCK)
