#!/usr/bin/python3

import dbus

bus = dbus.SystemBus()

SERVICE_NAME = 'org.bluez'
MANAGER_IFACE = 'org.freedesktop.DBus.ObjectManager'

manager = dbus.Interface(bus.get_object(SERVICE_NAME, '/'), MANAGER_IFACE)
objects = manager.GetManagedObjects()

for path, ifaces in objects.items():
    print(path)
    print(ifaces)
    

adapter = dbus.Interface(bus.get_object('org.bluez', manager.DefaultAdapter()), 'org.bluez.Adapter')
