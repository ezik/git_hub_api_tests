from pytest import fixture
from config import Config


@fixture(scope='session', autouse=True)
def app_config():
    config = Config()
    return config
