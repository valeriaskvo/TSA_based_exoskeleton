from machine import CAN

from config import *
from pins import BIT_1, BIT_2, BIT_3

sensors = {
    IMU_ID_1: None,
    IMU_ID_2: None,
    ENCODER_ID_1: None,
    ENCODER_ID_2: None,
    FORCE_ID_1: None,
    FORCE_ID_2: None
}


class Robot:

    def __init__(self):
        self.board_id = BOARD_ID \
                        + BIT_1.value() * (2 ** 2) \
                        + BIT_2.value() * (2 ** 1) \
                        + BIT_3.value() * (2 ** 0)

    def run(self, __can: CAN):
        while True:
            if __can.any():
                packet = __can.recv()
                data = list(packet[-1])[0]

                func = sensors.get(data)

                if func is not None:
                    func()
