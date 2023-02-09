from machine import Pin

# CAN bus pins
CAN_TX = Pin(26)
CAN_RX = Pin(27)

# I2C Interface Pins
I2C_SCL = Pin(18)
I2C_SDA = Pin(19)

# Switch Pins to detect device id = BIT_1 * 4 + BIT_2 * 2 + BIT_3 * 1

BIT_1 = Pin(8, Pin.IN)
BIT_2 = Pin(15, Pin.IN)
BIT_3 = Pin(2, Pin.IN)

# Force Sensor Pin

FORCE_SENSOR = Pin(4)

# Encoder Pins

ENC_A1 = Pin(34, Pin.IN)
ENC_B1 = Pin(35, Pin.IN)

ENC_A2 = Pin(32, Pin.IN)
ENC_B2 = Pin(33, Pin.IN)
