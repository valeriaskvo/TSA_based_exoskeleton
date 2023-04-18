from machine import Pin

# CAN bus pins
CAN_TX = 26
CAN_RX = 27

# I2C Interface Pins
I2C_SCL = Pin(19)
I2C_SDA = Pin(18)

# Switch Pins to detect device id = BIT_1 * 4 + BIT_2 * 2 + BIT_3 * 1

BIT_1 = Pin(8)
BIT_2 = Pin(15)
BIT_3 = Pin(2)

# Force Sensor Pin

FORCE_SENSOR_1 = Pin(36)
FORCE_SENSOR_2 = Pin(39)

# Encoder Pins

ENC_A1 = 34
ENC_B1 = 35

ENC_A2 = 32
ENC_B2 = 33
