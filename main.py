import asyncio
import bluetooth_sensor
import gpio_sensor
from rx import typing
from rx.disposable.compositedisposable import CompositeDisposable
import logging
import logging.config

logging.config.fileConfig('logging.conf')

loop = asyncio.get_event_loop()
loop.set_debug(True)

READING_INTERVAL = 60.0


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


disposable = CompositeDisposable(
    bluetooth_sensor.observe(interval=READING_INTERVAL).subscribe(ReadingsObserver('Kitchen')),
    gpio_sensor.observe(interval=READING_INTERVAL).subscribe(ReadingsObserver('Living room'))
)

print('Started.')

while True:
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        logging.warning('Main loop interrupted.')

        disposable.dispose()
        loop.close()
