import smbus
bus = smbus.SMBus(1)

MODE1 = 0x00
MODE2 = 0x01
PRE_SCALE = 0xfe
LED0_ON_L = 0x06
LED0_OFF_L = 0x08
LED1_ON_L = 0x0a
LED1_OFF_L = 0x0c

PWM_200HZ = 30
PWM_50HZ = 121

addr = 0x40

print(bus.read_byte_data(addr, MODE1))
bus.write_byte_data(addr, MODE1, 0x10)
bus.write_byte_data(addr, PRE_SCALE, PWM_50HZ)
bus.write_byte_data(addr, MODE1, 0x20)
print(bus.read_byte_data(addr, MODE1))

while True:
  [ pan, tilt ] = map(int, raw_input().strip().split(" "))
  print(tilt)

  bus.write_word_data(addr, LED0_ON_L, 0)
  bus.write_word_data(addr, LED0_OFF_L, pan)

  bus.write_word_data(addr, LED1_ON_L, 0)
  bus.write_word_data(addr, LED1_OFF_L, tilt)

