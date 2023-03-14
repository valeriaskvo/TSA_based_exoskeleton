import os

import can
import matplotlib.pyplot as plt
import numpy as np

from config import *

bustype = 'socketcan'
channel = 'can0'

os.system('sudo slcand -o -c -s8 -S 115200 /dev/ttyACM0 can0')
os.system('sudo ifconfig can0 down')
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system(f'sudo ifconfig can0 up')
os.system(f'sudo ifconfig can0 txqueuelen 65536')

bus = can.interface.Bus(channel=channel, bustype=bustype)


def bytes_to_int(firstbyte, secondbyte):
    """
    returned in range of Int16
    -32768 to 32767
    """
    if not firstbyte & 0x80:
        return firstbyte << 8 | secondbyte
    return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)


imu_data = dict()


def imu(msg: can.Message) -> None:
    global imu_data
    board_id = msg.arbitration_id
    device_id, flag, *data = list(msg.data)
    ax, ay, az = bytes_to_int(data[0], data[1]), bytes_to_int(data[2], data[3]), bytes_to_int(data[4], data[5])
    name = "Acceleration" if flag == 48 else "Gyroscope"
    print(f"Device {board_id}: {name}-{device_id} <{ax}, {ay}, {az}>")

    if imu_data.get(device_id) is None:
        imu_data.update({device_id: dict()})
        imu_data[device_id].update({IMU_ACCEL: [], IMU_GYRO: []})

    imu_data[device_id][flag].append([ax, ay, az])


force_data = []


def force(msg: can.Message) -> None:
    global force_data
    board_id = msg.arbitration_id
    device_id, flag, *data = list(msg.data)
    data = msg.data[-2:]
    mass_raw = int.from_bytes(data, "little", signed=True)
    print(f"Device {board_id}: {device_id} with mass {mass_raw / 65535}")
    force_data.append(mass_raw / 65535)


try:
    while True:
        msg = bus.recv()
        if msg:
            board_id = msg.arbitration_id
            device_id, flag, *data = list(msg.data)

            if device_id in [IMU_ID_1, IMU_ID_2]:
                imu(msg)

            if device_id in [FORCE_ID_1, FORCE_ID_2]:
                force(msg)

except KeyboardInterrupt:
    os.system('sudo ifconfig can0 down')
    raw = np.array(force_data)
    plt.figure(figsize=(18, 6))
    plt.plot(raw)
    plt.grid(True, linestyle="--", linewidth=1, alpha=0.7)
    plt.savefig("force.png")
    plt.show()

    fig, axes = plt.subplots(2, 2, figsize=(18, 6))

    for i, (sens, dt) in enumerate(imu_data.items()):
        for j, (flag, ddt) in enumerate(dt.items()):
            dr = np.array(ddt)
            axes[i][j].set_title(f"Sensor {sens} with flag {flag}")
            axes[i][j].plot(dr[:, 0], label="x")
            axes[i][j].plot(dr[:, 1], label="y")
            axes[i][j].plot(dr[:, 2], label="z")
            axes[i][j].grid(True, linestyle="--", linewidth=1, alpha=0.7)
            axes[i][j].legend()
    plt.savefig("imu.png")
    plt.show()

except Exception as e:
    os.system('sudo ifconfig can0 down')
    print(e)
