from django.apps import apps
from theatre.apps import TheatreConfig


def test_theatre_config_loaded():
    config = apps.get_app_config("theatre")
    assert isinstance(config, TheatreConfig)
    assert config.label == "theatre"
    assert config.name == "theatre"
