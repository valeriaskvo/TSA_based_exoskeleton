from machine import CAN, SoftI2C

from config import *
from encoder_sensor import Encoder
from force_sensor import ForceSensor
from imu_sensor import IMUSensor
from pins import *

# ================== Interfaces ==================
i2c = SoftI2C(scl=I2C_SCL, sda=I2C_SDA)
can = CAN(0, tx=CAN_TX, rx=CAN_RX, extframe=False, mode=CAN.LOOPBACK, baudrate=1000000)

# ================== Sensors ==================

sensors = {
    IMU_ID_1: IMUSensor(i2c, can, IMU_ID_1),
    IMU_ID_2: IMUSensor(i2c, can, IMU_ID_2),
    ENCODER_ID_1: Encoder(ENCODER_ID_1, ENC_A1, ENC_B1, can),
    ENCODER_ID_2: Encoder(ENCODER_ID_2, ENC_A2, ENC_B2, can),
    FORCE_ID_1: ForceSensor(FORCE_ID_1, FORCE_SENSOR_1, can),
    FORCE_ID_2: ForceSensor(FORCE_ID_2, FORCE_SENSOR_2, can)
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
                if packet[1] and packet[0] == self.board_id:
                    data = list(packet[-1])[0]

                    sensor = sensors.get(data)

                    if sensor is not None:
                        try:
                            sensor.send(self.board_id)
                        except:
                            __can.send([sensor.device_id, 404, 0, 0, 0, 0, 0, 0], self.board_id)
                            __can.clear_rx_queue()
                            __can.clear_tx_queue()
