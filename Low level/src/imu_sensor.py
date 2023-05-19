from machine import I2C, CAN

from can_interface import CanBus, encode
from config import IMU_GYRO, IMU_ACCEL


class IMUSensor:

    def __init__(self, i2c: I2C, can: CAN, address: int) -> None:
        self._can = CanBus(can)
        self._i2c = i2c
        self.address = address
        self._i2c.start()
        self._i2c.writeto(self.address, bytearray([107, 0]))
        self._i2c.stop()
        self.device_id = address

    def __del__(self) -> None:
        self._can.__del__()
        self._i2c.deinit()

    def get_raw_values(self) -> bytes:
        self._i2c.start()
        a = self._i2c.readfrom_mem(self.address, 0x3B, 14)
        self._i2c.stop()
        return a

    def get_ints(self) -> list:
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def send(self, board_id: int) -> None:
        data = self.get_ints()
        acceleration = encode(self.address, data=data[:6], device_flag=IMU_ACCEL)
        gyroscope = encode(self.address, data=data[8:], device_flag=IMU_GYRO)
        self._can.send(board_id, acceleration)
        self._can.send(board_id, gyroscope)
