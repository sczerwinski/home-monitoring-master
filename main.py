import bluetooth_sensor
import gpio_sensor
import app_config as conf
import asyncio
from rx import typing
from rx.disposable.compositedisposable import CompositeDisposable
import logging
import logging.config

logging.config.fileConfig('logging.conf')

loop = asyncio.get_event_loop()
loop.set_debug(True)

READING_INTERVAL = conf.main_interval()
BLUETOOTH_NAME = conf.main_bluetooth_name()
GPIO_NAME = conf.main_gpio_name()


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
    bluetooth_sensor.observe(interval=READING_INTERVAL).subscribe(ReadingsObserver(BLUETOOTH_NAME)),
    gpio_sensor.observe(interval=READING_INTERVAL).subscribe(ReadingsObserver(GPIO_NAME))
)

print('Started.')

while True:
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        logging.warning('Main loop interrupted.')

        disposable.dispose()
        loop.close()
