import struct

import dbus
import smbus


from service import Service
from characteristic import Characteristic
from descriptor import Descriptor, CharacteristicUserDescriptionDescriptor

from pan_tilt import PanTilt

I2C_BUS_NUMBER = 1

# with none of the 6 address jumpers closed, base address is
# 1 0 0 0 0 0 0 W
# except that library manages W bit
addr = 0x40

bus = smbus.SMBus(I2C_BUS_NUMBER)
adapter = PanTilt(bus, addr)
adapter.initialize_channels()
# adapter.setBias([ 225, 225 ])
print("pan tilt initialized")

class RobbyService(Service):
    """
    Dummy test service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    TEST_SVC_UUID = '12345678-1234-5678-1234-56789abcdef0'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.TEST_SVC_UUID, True)
        self.add_characteristic(TestCharacteristic(bus, 0, self))
        # self.add_characteristic(TestEncryptCharacteristic(bus, 1, self))
        # self.add_characteristic(TestSecureCharacteristic(bus, 2, self))

class TestCharacteristic(Characteristic):
    """
    Dummy test characteristic. Allows writing arbitrary bytes to its value, and
    contains "extended properties", as well as a test descriptor.

    """
    TEST_CHRC_UUID = '12345678-1234-5678-1234-56789abcdef1'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.TEST_CHRC_UUID,
            ['read', 'write', 'writable-auxiliaries'],
            service)
        self.value = []
        self.add_descriptor(TestDescriptor(bus, 0, self))
        self.add_descriptor(
            CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        print('TestCharacteristic Read: ' + repr(self.value))
        return self.value

    # assume little endian order
    # pan and tilt are each 16 bits, but range is only 12 bits
    def WriteValue(self, value, options):
        # print('TestCharacteristic Write: ' + repr(value))
        self.value = value
        try:
            (pan, tilt) = struct.unpack("< h h", bytes(value))
            # print(pan, tilt)
        except Exception as err:
            print("unpack err: {}".format(err))
        # pan = int(value[0] )
        # tilt = int(value[2])
        adapter.moveTo(pan, tilt)

class TestDescriptor(Descriptor):
    """
    Dummy test descriptor. Returns a static value.

    """
    TEST_DESC_UUID = '12345678-1234-5678-1234-56789abcdef2'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.TEST_DESC_UUID,
            ['read', 'write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]

class TestEncryptCharacteristic(Characteristic):
    """
    Dummy test characteristic requiring encryption.

    """
    TEST_CHRC_UUID = '12345678-1234-5678-1234-56789abcdef3'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.TEST_CHRC_UUID,
            ['encrypt-read', 'encrypt-write'],
            service)
        self.value = []
        self.add_descriptor(TestEncryptDescriptor(bus, 2, self))
        self.add_descriptor(
            CharacteristicUserDescriptionDescriptor(bus, 3, self))

    def ReadValue(self, options):
        print('TestEncryptCharacteristic Read: ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('TestEncryptCharacteristic Write: ' + repr(value))
        self.value = value

class TestEncryptDescriptor(Descriptor):
    """
    Dummy test descriptor requiring encryption. Returns a static value.

    """
    TEST_DESC_UUID = '12345678-1234-5678-1234-56789abcdef4'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.TEST_DESC_UUID,
            ['encrypt-read', 'encrypt-write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class TestSecureCharacteristic(Characteristic):
    """
    Dummy test characteristic requiring secure connection.

    """
    TEST_CHRC_UUID = '12345678-1234-5678-1234-56789abcdef5'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.TEST_CHRC_UUID,
            ['secure-read', 'secure-write'],
            service)
        self.value = []
        self.add_descriptor(TestSecureDescriptor(bus, 2, self))
        self.add_descriptor(
            CharacteristicUserDescriptionDescriptor(bus, 3, self))

    def ReadValue(self, options):
        print('TestSecureCharacteristic Read: ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('TestSecureCharacteristic Write: ' + repr(value))
        self.value = value


class TestSecureDescriptor(Descriptor):
    """
    Dummy test descriptor requiring secure connection. Returns a static value.

    """
    TEST_DESC_UUID = '12345678-1234-5678-1234-56789abcdef6'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.TEST_DESC_UUID,
            ['secure-read', 'secure-write'],
            characteristic)

    def ReadValue(self, options):
        return [
            dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]
