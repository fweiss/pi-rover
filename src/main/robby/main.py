#!/usr/bin/env python3

# source: bluez/test/example-gatt-server.py,
# bluez/test/example-advertisement.py

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import sys

from advertisement import Advertisement
from battery_service import BatteryService
from robby_service import RobbyService
from heart_rate_service import HeartRateService

mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'

LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'

class Application(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
        # self.add_service(HeartRateService(bus, 0))
        # self.add_service(BatteryService(bus, 1))
        self.add_service(RobbyService(bus, 2))

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            print("adding service: {}".format(service.get_path()))
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()

        return response

def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None

class RoverAdvertisement(Advertisement):

    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid('180D')
        self.add_service_uuid('180F')
        # self.add_manufacturer_data(0xffff, [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_service_data('9999', [0x00, 0x01, 0x02, 0x03, 0x04])
        self.add_local_name('Rover')
        self.include_tx_power = True
        # self.add_data(0x26, [0x01, 0x01, 0x00])


def register_ad_cb():
    global advertisementRegistered
    print('Advertisement registered')
    advertisementRegistered = True

def register_ad_error_cb(error):
    global advertisementRegistered
    print('RegisterAdvertisement: {}'.format(str(error)))
    advertisementRegistered = False
    mainloop.quit()

def device_connect_cb(prop):
    print('device connect')

def interfaces_removed_cb(object_path, interfaces):
    print('Service was removed')

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    # device = bus.get_object('org.bluez', '/hci0')
    # device.connect_to_signal('connect', device_connect_cb)
    # bus.add_signal_receiver(device_connect_cb, bus_name="org.bluez", signal_name="PropertyChanged", dbus_interface="org.bluez.Device", path_keyword="path", interface_keyword="interface")

    # om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
    # om.connect_to_signal('InterfacesRemoved', interfaces_removed_cb)
    # om.connect_to_signal('RemoteDeviceFound', interfaces_removed_cb)

    # om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_PROP_IFACE)
    # om.connect_to_signal('PropertiesChanged', device_connect_cb)

    service_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter),
        GATT_MANAGER_IFACE)

    app = Application(bus)

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    test_advertisement = RoverAdvertisement(bus, 0)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    try:
        mainloop.run()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        global advertisementRegistered
        if advertisementRegistered:
            ad_manager.UnregisterAdvertisement(test_advertisement)
            print('Advertisement unregistered')
            dbus.service.Object.remove_from_connection(test_advertisement)

if __name__ == '__main__':
    main()
