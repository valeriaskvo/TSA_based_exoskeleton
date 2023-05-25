from dataclasses import dataclass
from time import perf_counter, time, sleep
from typing import List

import numpy as np

from includes import CanBus

BOARD_ID = 0x130
ENCODER_ID_1 = 0x18  # Encoder
ENCODER_ID_2 = 0x19  # Encoder


@dataclass
class Packet:
    id: int
    flag: int
    data: List[int]
    timestamp: float


def decode(data: List[int]) -> Packet:
    idx, flag, *buffer = data
    x = int.from_bytes(buffer[-2:], "little", signed=True)
    return Packet(idx, flag, [x], time())


t_total = float(input("Set total time to read data [seconds]: "))
bus = CanBus()

try:
    packets = []

    print("""
        Press enter to start reading
        """)
    input()

    t0 = perf_counter()
    while perf_counter() - t0 <= t_total:
        data = bus.request(BOARD_ID, [ENCODER_ID_1, 0, 0, 0, 0, 0, 0, 0])[0].data
        b = decode(data)
        packets.append([b.timestamp, b.data[0]])
        sleep(0.00001)  # freq = 100 kHz

    np.savetxt("./data/encoder.csv", np.array(packets))

except KeyboardInterrupt:
    pass
finally:
    bus.close()
