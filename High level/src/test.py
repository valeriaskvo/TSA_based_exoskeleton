import os
from time import time

import can

from config import *

bustype = 'socketcan'
channel = 'can0'

os.system('sudo slcand -o -c -s8 -S 115200 /dev/ttyACM2 can0')
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


def imu(msg: can.Message) -> None:
    board_id = msg.arbitration_id
    device_id, flag, *data = list(msg.data)
    ax, ay, az = bytes_to_int(data[0], data[1]), bytes_to_int(data[2], data[3]), bytes_to_int(data[4], data[5])
    name = "Acceleration" if flag == 48 else "Gyroscope"
    print(f"Device {board_id}: {name}-{device_id} <{ax}, {ay}, {az}>")


def send_recv(idx, bus: can.interface.Bus, timeout=1, count=2):
    msg = can.Message(
        arbitration_id=0x400,
        dlc=8,
        data=[idx, 0, 0, 0, 0, 0, 0, 0]
    )
    bus.send(msg)
    ans = []
    st_time = time()
    while True:
        if time() - st_time >= timeout:
            bus.send(msg)
            st_time = time()
        recv = bus.recv(0.1)

        if recv:
            ans.append(recv)

        if len(ans) == count:
            return ans


try:
    print("""
        Hello there, let's get the information from ESP
         1. IMU 1
         2. IMU 2
         3. Encoder 3
        """)
    while True:
        cmd = int(input("Command number: "))
        count = int(input("How many packets you want: "))
        ans = []

        for i in range(count):
            if cmd == 1:
                ans.extend(send_recv(IMU_ID_1, bus))

            if cmd == 2:
                ans.extend(send_recv(IMU_ID_2, bus))

            if cmd == 3:
                ans.extend(send_recv(ENCODER_ID_1, bus, count=1))

        if cmd != 3:
            print("=" * 20)
            for i, a in enumerate(ans):
                if i % 2 == 0:
                    print(f"Packet Number: {i // 2 + 1}")
                imu(a)
            print("=" * 20)
        else:
            print("=" * 20)
            for i, a in enumerate(ans):
                print(f"Packet Number: {i + 1}")
                d = list(a.data)[-2:]
                x = int.from_bytes(d, "little", signed=True)
                print(x)
            print("=" * 20)

except Exception as e:
    os.system('sudo ifconfig can0 down')
    print(e)
