# Home Monitoring – Master Raspberry Pi

## Configuration

Create file `app.conf` to set up the script, e.g.:

```properties
[main]
interval=60.0
bluetooth_name=Kitchen
gpio_name=Living room

[bluetooth]
address=00:15:83:00:9F:FA
uuid=0000ffe1-0000-1000-8000-00805f9b34fb

[server]
base_url=http://localhost/home-monitoring/api
```

`[main]`:
* `interval` – sensor readings interval (default `60.0`)
* `bluetooth_name` – name of the location for the [Arduino](/sczerwinski/home-monitoring-slave)
* `gpio_name` – name of the location for the Raspberry Pi

`[bluetooth]`:
* `address` – BLE device address used to connect to the [Arduino](/sczerwinski/home-monitoring-slave)
* `uuid` – BLE device characteristic UUID, used by [Arduino](/sczerwinski/home-monitoring-slave) to send sensor readings

`[server]`:
* `base_url` – base URL of the [REST API](/sczerwinski/home-monitoring-server)
