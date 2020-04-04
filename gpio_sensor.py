from adafruit_dht import DHT22
from board import D18 as DHT_PIN
import rx
from rx import operators as ops

_dhtDevice = DHT22(DHT_PIN)

READING_INTERVAL = 10.0


def _get_sensor_reading():
    try:
        humidity = _dhtDevice.humidity
        temperature = _dhtDevice.temperature

        if humidity is not None and temperature is not None:
            return {'humidity': humidity, 'temperature': temperature}
        else:
            return {'error': 'Failed to retrieve data from sensor'}

    except RuntimeError as err:
        return {'error': err}


def observe():
    return rx.interval(READING_INTERVAL).pipe(
        ops.map(lambda value: _get_sensor_reading()),
        ops.filter(lambda value: 'error' not in value)
    )
