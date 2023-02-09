from time import sleep

from machine import SoftI2C, Pin, CAN, reset

from IMU import IMU
from can import CanIMUMessage

reset()  # To clear buffer for CAN bus

i2c = SoftI2C(scl=Pin(18), sda=Pin(19))
CAN_TX = 26
CAN_RX = 27

interface = CAN(0, tx=CAN_TX, rx=CAN_RX, extframe=False, mode=CAN.NORMAL, baudrate=1000000)
imu = IMU(i2c, imu_id=2)
msg = CanIMUMessage(imu)

while True:
    print("=" * 7)
    interface.send(msg.get_acceleration(), 0x130)
    interface.send(msg.get_gyroscope(), 0x130)
    interface.clear_rx_queue()
    interface.clear_tx_queue()
    sleep(1)
