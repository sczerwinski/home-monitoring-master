import time
import bluetooth_sensor
import gpio_sensor
from rx import operators as ops
from rx import typing
from datetime import datetime


class ReadingsObserver(typing.Observer):

    def __init__(self, location):
        self._location = location

    def on_next(self, value):
        print("%s\t%s:\t%s" % (datetime.now().strftime("%H:%M:%S"), self._location, value))

    def on_error(self, err):
        print(err)

    def on_completed(self):
        print('completed')


bluetooth_sensor.observe().pipe(
    ops.throttle_first(60.0)
).subscribe(ReadingsObserver("Kitchen"))

gpio_sensor.observe().pipe(
    ops.throttle_first(60.0)
).subscribe(ReadingsObserver("Living room"))

while True:
    time.sleep(10)
