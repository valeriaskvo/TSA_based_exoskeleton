from machine import SoftI2C, Pin, CAN, Timer
from imu_sensor import IMUSensor
from force_sensor import ForceSensor
from config import *

i2c = SoftI2C(scl=Pin(18), sda=Pin(19))
interface = CAN(0, tx=26, rx=27, extframe=False, mode=CAN.NORMAL, baudrate=1000000)

sensor_1 = IMUSensor(i2c, interface, IMU_ID_1)
sensor_2 = IMUSensor(i2c, interface, IMU_ID_2)
sensor_3 = ForceSensor(FORCE_ID_1, 34, interface)

tim1 = Timer(0)
tim2 = Timer(1)
tim3 = Timer(2)

tim1.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_1.send(BOARD_ID))
tim2.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_2.send(BOARD_ID))
tim3.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_3.send(BOARD_ID))
