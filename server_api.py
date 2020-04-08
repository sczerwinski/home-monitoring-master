import app_config as conf
import requests
from rx import typing
import logging

API_POST_READING_URL = '/location/{location_name}/type/{sensor_type}/reading'


class ReadingsObserver(typing.Observer):

    def __init__(self, location):
        self._location = location
        self._url = conf.server_base_url() + API_POST_READING_URL
        self.log = logging.getLogger('%s[%s]' % (__name__, location))

    def _post_reading(self, sensor_type, value):
        request_url = self._url.format(
            location_name=requests.utils.quote(self._location),
            sensor_type=sensor_type
        )
        self.log.debug("-> POST %s", request_url)
        self.log.debug("body: %f", value)
        request = requests.post(url=request_url, json=value)
        self.log.debug("<- %d %s", request.status_code, request_url)
        self.log.debug(request.content)

    def on_next(self, value):
        self.log.info(value)
        for sensor_type, reading_value in value.items():
            self._post_reading(sensor_type, reading_value)

    def on_error(self, err):
        self.log.critical(err)

    def on_completed(self):
        self.log.warning('Execution completed')
