from IMU import IMU
from can_config import *


class CanIMUMessage:
    def __init__(self, imu: IMU) -> None:
        self.device_id = imu.addr
        self.imu = imu

    def get_acceleration(self) -> list:
        data = self.imu.get_ints()[:6]
        print(data)
        msg = [self.device_id, IMU_ACCEL]
        msg.extend(data)
        return msg

    def get_gyroscope(self) -> list:
        data = self.imu.get_ints()[8:]
        print(data)
        msg = [self.device_id, IMU_GYRO]
        msg.extend(data)
        return msg
