from pytest_factoryboy import register

from tests.factories import BoardFactory

pytest_plugins = 'tests.fixtures'

register(BoardFactory)
