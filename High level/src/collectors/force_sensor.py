from dataclasses import dataclass
from time import perf_counter, time, sleep
from typing import List
import numpy as np
from includes import CanBus

BOARD_ID = 0x130
FORCE_ID_1 = 0x28  # Force sensor
FORCE_ID_2 = 0x29  # Force sensor


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
t_baseline = float(input("Set time to read baseline [seconds]: "))
bus = CanBus()

try:
    packets: List[int] = []

    print("""
    Put out the load from the sensor to read baseline data.
    Press enter to start reading
    """)
    input()

    t0 = perf_counter()
    while perf_counter() - t0 <= t_baseline:
        data = bus.request(BOARD_ID, [FORCE_ID_2, 0, 0, 0, 0, 0, 0, 0])[0].data
        packets.append(decode(data).data[0])
        sleep(0.00001)  # freq = 100 kHz

    packets.append(-1)
    print("""
        Put in the load to the sensor to read data.
        Press enter to start reading
        """)
    input()

    t0 = perf_counter()
    while perf_counter() - t0 <= t_total - t_baseline:
        data = bus.request(BOARD_ID, [FORCE_ID_2, 0, 0, 0, 0, 0, 0, 0])[0].data
        packets.append(decode(data).data[0])
        sleep(0.00001)  # freq = 100 kHz

    values = np.array(packets)
    delimiter = np.argwhere(values == -1)[0][0]

    baseline = values[:delimiter]
    total = values[delimiter+1:]

    ts_baseline = np.linspace(0, t_baseline, baseline.shape[0])
    ts_total = np.linspace(t_baseline, t_total, total.shape[0])

    bb = np.vstack([ts_baseline, baseline]).T
    bt = np.vstack([ts_total, total]).T

    data = np.vstack([bb, bt])
    np.savetxt("./data/force.csv", data)

except KeyboardInterrupt:
    pass
finally:
    bus.close()
