import time
import bluetooth_sensor
import gpio_sensor
from rx import operators as ops
from rx import typing
import logging
import logging.config

logging.config.fileConfig('logging.conf')


class ReadingsObserver(typing.Observer):

    def __init__(self, location):
        self._location = location
        self.log = logging.getLogger('%s(%s)' % (self.__class__.__name__, location))

    def on_next(self, value):
        self.log.info(value)

    def on_error(self, err):
        self.log.critical(err)

    def on_completed(self):
        self.log.warning('Execution completed')


bluetooth_sensor.observe().pipe(
    ops.throttle_first(60.0)
).subscribe(ReadingsObserver('Kitchen'))

gpio_sensor.observe().pipe(
    ops.throttle_first(60.0)
).subscribe(ReadingsObserver('Living room'))

print('Started.')

while True:
    time.sleep(10)
