import bluetooth_sensor
import gpio_sensor
import server_api
import app_config as conf
import asyncio
from rx.disposable.compositedisposable import CompositeDisposable
import logging.config

logging.config.fileConfig('logging.conf')

loop = asyncio.get_event_loop()
loop.set_debug(True)

READING_INTERVAL = conf.main_interval()
BLUETOOTH_LOCATION_NAME = conf.main_bluetooth_name()
GPIO_LOCATION_NAME = conf.main_gpio_name()

disposable = CompositeDisposable(
    bluetooth_sensor.observe(interval=READING_INTERVAL).subscribe(
        observer=server_api.ReadingsObserver(location=BLUETOOTH_LOCATION_NAME)
    ),
    gpio_sensor.observe(interval=READING_INTERVAL).subscribe(
        observer=server_api.ReadingsObserver(location=GPIO_LOCATION_NAME)
    )
)

print('Started.')

while True:
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        logging.warning('Main loop interrupted.')

        disposable.dispose()
        loop.close()
