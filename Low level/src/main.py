# from machine import SoftI2C, Pin, CAN
#
# from config import *
# from encoder_sensor import Encoder
# from force_sensor import ForceSensor
# from imu_sensor import IMUSensor
# from time import sleep_ms
#
# i2c = SoftI2C(scl=Pin(19), sda=Pin(18))
# interface = CAN(0, tx=26, rx=27, extframe=False, mode=CAN.LOOPBACK, baudrate=1000000)
#
# # sensor_1 = IMUSensor(i2c, interface, IMU_ID_1)
# # sensor_2 = IMUSensor(i2c, interface, IMU_ID_2)
# # sensor_4 = Encoder(ENCODER_ID_1, 34, 35, interface)
# sensor_3 = ForceSensor(FORCE_ID_1, 36, interface)
#
# # tim1 = Timer(0)
# # tim2 = Timer(1)
# # tim3 = Timer(2)
#
# # tim1.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_1.send(BOARD_ID))
# # tim2.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_2.send(BOARD_ID))
# # tim3.init(mode=Timer.PERIODIC, period=1, callback=lambda t: sensor_3.send(BOARD_ID))
#
# while True:
#     # if interface.any():
#     #     packet = interface.recv()
#     #     if packet[1]:
#     #         data = list(packet[-1])[0]
#     #
#     #         if data == IMU_ID_1:
#     #             sensor_1.send(0x130)
#     #
#     #         if data == IMU_ID_2:
#     #             sensor_2.send(0x130)
#     #
#     #         if data == ENCODER_ID_1:
#     #             sensor_4.send(0x130)
#     #
#     #         if data == FORCE_ID_1:
#     #             sensor_3.send(0x130)
#     print(sensor_3.sensor.read_u16())
#     sleep_ms(100)

from source import can, Robot

board = Robot()
board.run(can)
