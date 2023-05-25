from dataclasses import dataclass
from time import time, sleep
from typing import List

import numpy as np

from config import *
from includes import Gyems, CanBus


@dataclass
class Packet:
    id: int
    flag: int
    data: List[int]
    timestamp: float


class Computer:
    def __init__(self, file_name: str, speed: int):
        self.can = CanBus()
        self.packets: List[Packet] = []
        self.file_name = file_name
        # self.motor = Gyems(self.can)
        # self.motor.enable()
        # self.motor.set_zero()
        self.motor_data = []
        self.speed = speed

    @staticmethod
    def bytes_to_int(firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def decode_imu(self, data: List[int]) -> Packet:
        idx, flag, *buffer = data
        x = self.bytes_to_int(buffer[0], buffer[1])
        y = self.bytes_to_int(buffer[2], buffer[3])
        z = self.bytes_to_int(buffer[4], buffer[5])
        return Packet(idx, flag, [x, y, z], time())

    @staticmethod
    def decode(data: List[int]) -> Packet:
        idx, flag, *buffer = data
        x = int.from_bytes(buffer[-2:], "little", signed=True)
        return Packet(idx, flag, [x], time())

    def save(self) -> None:
        data = dict()
        for packet in self.packets:
            if data.get(f"{packet.id} {packet.flag}") is not None:
                data[f"{packet.id} {packet.flag}"].append(packet)
            else:
                data.update({f"{packet.id} {packet.flag}": [packet]})

        for key in data.keys():
            data[key].sort(key=lambda x: x.timestamp)

        min_timestamp = np.inf
        max_timestamp = -np.inf

        for value in self.packets:
            min_timestamp = min(min_timestamp, value.timestamp)
            max_timestamp = max(max_timestamp, value.timestamp)

        ts = np.linspace(0, max_timestamp - min_timestamp, len(self.packets) // 6)

        headers_dict = [
            f"{IMU_ID_1} {IMU_ACCEL}",
            f"{IMU_ID_1} {IMU_GYRO}",
            f"{IMU_ID_2} {IMU_ACCEL}",
            f"{IMU_ID_2} {IMU_GYRO}",
            f"{ENCODER_ID_1} {0}",
            f"{ENCODER_ID_2} {0}",
            f"{FORCE_ID_1} {0}",
            f"{FORCE_ID_2} {0}",
        ]

        headers = [
            "timestamp",
            "imu_1_accel x",
            "imu_1_accel y",
            "imu_1_accel z",
            "imu_1_gyro x",
            "imu_1_gyro y",
            "imu_1_gyro z",
            "imu_2_accel x",
            "imu_2_accel y",
            "imu_2_accel z",
            "imu_2_gyro x",
            "imu_2_gyro y",
            "imu_2_gyro z",
            "encoder_1",
            "encoder_2",
            "force_1",
            "force_2",
        ]

        combat = list(zip(
            ts,
            data[headers_dict[0]],
            data[headers_dict[1]],
            data[headers_dict[2]],
            data[headers_dict[3]],
            data[headers_dict[4]],
            data[headers_dict[5]],
            data[headers_dict[6]],
            data[headers_dict[7]],
        ))

        result = []

        for l in combat:
            buffer = [l[0], *[f.data for f in l[1:]]]
            r = []
            for i in buffer:
                if isinstance(i, list):
                    r.extend(i)
                else:
                    r.append(i)
            result.append(r)

        a = np.asarray(result)
        np.savetxt(f"data/{self.file_name}", a, delimiter=";", header=";".join(headers))

        # headers = list(self.motor_data[0].keys())
        # data = np.asarray([list(f.values()) for f in self.motor_data])
        # np.savetxt(f"data/motor_{self.file_name}", data, delimiter=";", header=";".join(headers))

    def run(self) -> None:
        # self.motor.set_speed(self.speed)
        try:
            while True:
                imu1 = self.can.request(BOARD_ID, [IMU_ID_1, 0, 0, 0, 0, 0, 0, 0], n_packets=2)
                imu2 = self.can.request(BOARD_ID, [IMU_ID_2, 0, 0, 0, 0, 0, 0, 0], n_packets=2)
                enc1 = self.can.request(BOARD_ID, [ENCODER_ID_1, 0, 0, 0, 0, 0, 0, 0])
                enc2 = self.can.request(BOARD_ID, [ENCODER_ID_2, 0, 0, 0, 0, 0, 0, 0])
                force1 = self.can.request(BOARD_ID, [FORCE_ID_1, 0, 0, 0, 0, 0, 0, 0])
                force2 = self.can.request(BOARD_ID, [FORCE_ID_2, 0, 0, 0, 0, 0, 0, 0])
                # state = self.motor.info()
                # self.motor_data.append(state)
                for response in [*imu1, *imu2, *enc1, *enc2, *force1, *force2]:
                    if response.data[0] in [IMU_ID_1, IMU_ID_2]:
                        self.packets.append(self.decode_imu(response.data))
                    else:
                        self.packets.append(self.decode(response.data))
                sleep(0.0001)
        except:
            pass
            # try:
            #     self.motor.set_speed(-self.speed)
            #     while self.motor.info()["angle"] > 0:
            #         continue
            #     self.motor.set_speed(0)
            # except:
            #     pass
        finally:
            self.close()
            self.save()

    def close(self):
        # self.motor.disable(True)
        # sleep(1)
        self.can.close()
        # print(self.motor.status)


if __name__ == '__main__':
    comp = Computer("result_test_lera.csv", 360)
    comp.run()
