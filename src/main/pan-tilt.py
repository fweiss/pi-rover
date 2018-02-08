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

def pulse_width(off):
    start = bus.read_word_data(addr,LED0_ON_L)
    stop = bus.read_word_data(addr, LED0_OFF_L)
    duty = (stop - start) / 4096.0
    prescale = bus.read_byte_data(addr, PRE_SCALE)
    osc_clock = 25000000.0
    pwm_freq = osc_clock / 4096.0 / (1.0 + prescale)
    pulse_width_ms = duty / pwm_freq * 1000.0
    return pulse_width_ms

while True:
    [ pan, tilt ] = map(int, raw_input().strip().split(" "))

    bus.write_word_data(addr, LED0_ON_L, 0)
    bus.write_word_data(addr, LED0_OFF_L, pan)
    print(pulse_width(pan))

    bus.write_word_data(addr, LED1_ON_L, 0)
    bus.write_word_data(addr, LED1_OFF_L, tilt)

