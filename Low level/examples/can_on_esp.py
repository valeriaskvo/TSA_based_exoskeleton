
from machine import CAN
from time import ticks_ms, ticks_us, sleep
import struct

CAN_TX = 26
CAN_RX = 27

can = CAN(0, tx=CAN_TX, rx=CAN_RX,
          extframe=False, mode=CAN.NORMAL,
          baudrate=1000000)

i = 0
while True:
    print('lol kek')
    if i == 0:
        command = struct.pack('f', 3.14)
        can.send(tuple(command), 0x1)    # send a message
        i = 1
    else:
        command = struct.pack('f', 1.1)
        can.send(tuple(command), 0x1)   # send a message
        i = 0
    can.clear_rx_queue()        # clear messages in the FIFO
    can.clear_tx_queue()  
    sleep(0.01)