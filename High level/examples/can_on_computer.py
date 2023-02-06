import sys
sys.path.append('../')

from can import CAN_Bus
from time import sleep
import struct

bus = CAN_Bus(interface='can0', devices_id=[0x001])

try:
    while True:
        can_id, can_dlc, can_data = bus.recive_frame()
        print(can_id, can_dlc)
        print(struct.unpack('f', can_data)[0])
except KeyboardInterrupt:
    print("End of work")
    pass