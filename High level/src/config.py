BOARD_ID = 0x132  # Board Id 0x130 + (0..8) ids
IMU_ID_1 = 0x68  # IMU sensor
IMU_ID_2 = 0x69  # IMU sensor
ENCODER_ID_1 = 0x18  # Encoder
ENCODER_ID_2 = 0x19  # Encoder
FORCE_ID_1 = 0x28  # Force sensor
FORCE_ID_2 = 0x29  # Force sensor

"""CAN Bus package for IMU Sensors
Package Structure:

[IMU_ID][IMU_RULE_ID][FIRST_BYTE_X][SECOND_BYTE_X][FIRST_BYTE_Y][SECOND_BYTE_Y][FIRST_BYTE_Z][SECOND_BYTE_Z]
"""

IMU_ACCEL = 0x30  # Flag get the accelerometer data
IMU_GYRO = 0x31  # Flag get the gyroscope data
