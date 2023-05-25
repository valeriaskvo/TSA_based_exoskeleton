from time import sleep

from config import FORCE_ID_1, FORCE_ID_2
from includes import CanBus

can = CanBus()
try:
    while True:
        data = can.request(0x130, [FORCE_ID_2, 0, 0, 0, 0, 0, 0, 0])[0].data[-2:]
        print(int.from_bytes(data, "little", signed=True))
        sleep(0.01)
except:
    pass
finally:
    can.close()
