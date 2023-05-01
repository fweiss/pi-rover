#!/usr/bin/python3

# https://github.com/karulis/pybluez

from bluetooth.ble import BeaconService

service = BeaconService()

SERVICE_UUID = '11111111-2222-3333-4444-555555555555'

service.start_advertising(SERVICE_UUID, 1, 1, 1, 200)

time.sleep(100)

service.stop_advertising()
