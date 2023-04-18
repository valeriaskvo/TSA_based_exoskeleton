from time import sleep

from includes.gyems import Gyems
from includes.interface import CanBus

bus = CanBus()
motor = Gyems(bus)

try:
    motor.enable()
    motor.set_zero()
    motor.set_current(0.1)
    while True:
        print(motor.info())
        sleep(0.1)
except KeyboardInterrupt:
    pass

finally:
    motor.disable(True)
    bus.close()
