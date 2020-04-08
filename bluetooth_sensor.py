import app_config as conf
import pygatt
import json
import rx
from rx import operators as ops
from rx.disposable import Disposable
from rx.scheduler import ThreadPoolScheduler, TimeoutScheduler
import logging

log = logging.getLogger(__name__)

_adapter = pygatt.GATTToolBackend()

_line = ''

MAX_THREAD_COUNT = 4


def _find_devices():
    print('Scanning...')
    return _adapter.scan()


def _find_named_devices():
    devices = _find_devices()
    return list(filter(lambda device: device['name'] is not None, devices))


def _print_devices(devices):
    print('Found devices:')
    for index, device in enumerate(devices):
        print('\t%d. %s (%s)' % (index + 1, device['name'], device['address']))


def _prompt_device_selection(devices):
    _print_devices(devices)
    count = len(devices)
    index = 1
    if count > 1:
        log.debug('Found multiple devices. Waiting for user input...')
        print('Select device [1-%d]:' % count, end='')
        index = int(input())
        log.debug('Selected device %s.', index)
    return devices[index - 1]


def _connect_ble_device_by_address(address):
    log.info('Connecting to device %s', address)
    return _adapter.connect(address)


def _connect_ble_device(device):
    return _connect_ble_device_by_address(address=device['address'])


def _get_characteristics(ble_device):
    uuids = list(ble_device.discover_characteristics().keys())
    uuids.sort()
    print('Found characteristics:')
    for uuid in uuids:
        print('\t* %s' % uuid)
    return uuids


def _subscribe_characteristic(ble_device, uuid, callback=None):
    log.info('Subscribing to characteristic %s', uuid)
    ble_device.subscribe(uuid, callback=callback)
    print('Subscribed to characteristic %s' % uuid)


def _rx_callback(value, observer):
    global _line
    _line += value.decode('utf-8')
    if _line.endswith('\n'):
        observer.on_next(_line)
        _line = ''


# noinspection PyUnusedLocal
def _subscribe(observer, scheduler):
    _adapter.start()

    config_address = conf.bluetooth_address()

    if config_address is None:
        named_devices = _find_named_devices()
        device = _prompt_device_selection(devices=named_devices)
        ble_device = _connect_ble_device(device)
    else:
        ble_device = _connect_ble_device_by_address(address=config_address)

    conf_uuid = conf.bluetooth_uuid()
    uuid = conf_uuid if conf_uuid is not None else _get_characteristics(ble_device)[-1]

    _subscribe_characteristic(ble_device, uuid, callback=lambda handle, value: _rx_callback(value, observer))

    def dispose():
        ble_device.unsubscribe(uuid)
        ble_device.disconnect()
        _adapter.stop()

    return Disposable(dispose)


def observe(interval=None):
    return rx.create(_subscribe).pipe(
        ops.map(lambda text: json.loads(text)),
        ops.sample(
            sampler=interval,
            scheduler=TimeoutScheduler.singleton()
        ) if interval is not None else lambda observable: observable,
        ops.observe_on(scheduler=ThreadPoolScheduler(MAX_THREAD_COUNT))
    )
