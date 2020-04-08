import configparser
import logging

log = logging.getLogger(__name__)

_config = configparser.ConfigParser()
_config.read('app.conf')


def _get_config_value(group, key, default):
    try:
        return _config[group][key]
    except KeyError:
        log.warning('No configuration value for [%s] %s', group, key)
        return default


def main_interval(default='60.0'):
    return float(_get_config_value('main', 'interval', default))


def main_bluetooth_name(default='Bluetooth'):
    return _get_config_value('main', 'bluetooth_name', default)


def main_gpio_name(default='GPIO'):
    return _get_config_value('main', 'gpio_name', default)


def bluetooth_address(default=None):
    return _get_config_value('bluetooth', 'address', default)


def bluetooth_uuid(default=None):
    return _get_config_value('bluetooth', 'uuid', default)


def server_base_url(default='http://localhost'):
    return _get_config_value('server', 'base_url', default)

