import pytest
import random
import json

from distconfig.confighandler import ConfigHandler
from distconfig.confighandler.parsers import JSONParser
from distconfig.caching import LocalLFUCache


config_handler = None
config_dict = {}


@pytest.fixture()
def fake_json(fs):  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    global config_handler
    global config_dict

    config_length = random.randint(0, 10)

    for _ in range(config_length):
        config_dict[str(random.randint(0, 100))] = str(random.randint(0, 100))

    fake_config_path = '/test_volume/servicename/config1.json'
    fs.create_file(fake_config_path, contents=json.dumps(config_dict))

    yield fs


def test_json_reading(fake_json):
    cache = LocalLFUCache(32)
    config_handler = ConfigHandler({'json': JSONParser}, '/test_volume', cache)
    test_config = config_handler.get_config('servicename', 'config1.json')

    assert len(config_dict) == len(test_config)
    assert sorted(config_dict.keys()) == sorted(test_config.keys())
    assert sorted(config_dict.values()) == sorted(test_config.values())
