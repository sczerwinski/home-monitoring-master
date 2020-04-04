import pygatt
import json
import rx
from rx import operators as ops
from rx.disposable import Disposable

_adapter = pygatt.GATTToolBackend()

_line = ''


def _find_devices():
    print('\nScanning...')
    return _adapter.scan()


def _find_named_devices():
    devices = _find_devices()
    return list(filter(lambda device: device['name'] is not None, devices))


def _print_devices(devices):
    print('\nFound devices:')
    for index, device in enumerate(devices):
        print("\t%d. %s (%s)" % (index + 1, device['name'], device['address']))


def _prompt_device_selection(devices):
    _print_devices(devices)
    count = len(devices)
    index = 1
    if count > 1:
        print("\nSelect device [1-%d]: " % count, end='')
        index = int(input())
    return devices[index - 1]


def _connect_ble_device_by_address(address):
    print("\nConnecting to device %s" % address)
    return _adapter.connect(address)


def _connect_ble_device(device):
    return _connect_ble_device_by_address(address=device['address'])


def _get_characteristics(ble_device):
    uuids = list(ble_device.discover_characteristics().keys())
    uuids.sort()
    print('\nFound characteristics:')
    for uuid in uuids:
        print("\t* %s" % uuid)
    return uuids


def _subscribe_characteristic(ble_device, uuid, callback=None):
    print("\nSubscribing to characteristic %s" % uuid)
    ble_device.subscribe(uuid, callback=callback)


def _rx_callback(value, observer):
    global _line
    _line += value.decode('utf-8')
    if _line.endswith('\n'):
        observer.on_next(_line)
        _line = ''


# noinspection PyUnusedLocal
def _subscribe(observer, scheduler):
    _adapter.start()
    named_devices = _find_named_devices()
    device = _prompt_device_selection(devices=named_devices)
    ble_device = _connect_ble_device(device)
    uuid = _get_characteristics(ble_device)[-1]
    _subscribe_characteristic(ble_device, uuid, callback=lambda handle, value: _rx_callback(value, observer))

    def dispose():
        _adapter.stop()

    return Disposable(dispose)


def observe():
    return rx.create(_subscribe).pipe(
        ops.map(lambda text: json.loads(text))
    )