from adafruit_dht import DHT22
from board import D18 as DHT_PIN
import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler, TimeoutScheduler
import logging

log = logging.getLogger(__name__)

_dhtDevice = DHT22(DHT_PIN)

READING_INTERVAL = 10.0
MAX_THREAD_COUNT = 4


def _get_sensor_reading():
    try:
        log.debug('Getting GPIO sensor reading')

        humidity = _dhtDevice.humidity
        temperature = _dhtDevice.temperature

        if humidity is not None and temperature is not None:
            return {'humidity': humidity, 'temperature': temperature}
        else:
            if humidity is None:
                log.warning('Could not retrieve humidity reading')
            if temperature is None:
                log.warning('Could not retrieve temperature reading')
            return {'error': 'Failed to retrieve data from sensor'}

    except RuntimeError as err:
        log.warning('Getting GPIO sensor reading failed: %s', err)
        return {'error': err}


def observe(interval=None):
    return rx.interval(
        period=READING_INTERVAL,
        scheduler=ThreadPoolScheduler(MAX_THREAD_COUNT)
    ).pipe(
        ops.map(lambda value: _get_sensor_reading()),
        ops.filter(lambda value: 'error' not in value),
        ops.sample(
            sampler=interval,
            scheduler=TimeoutScheduler.singleton()
        ) if interval is not None else lambda observable: observable
    )
