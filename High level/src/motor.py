from time import sleep, perf_counter

from includes import Gyems, CanBus

bus = CanBus()
motor = Gyems(bus)

try:
    motor.enable()
    motor.set_zero()
    motor.set_angle(360, 36)
    sleep(10)

    # while True:
    #     print(motor.info())
    #     sleep(0.1)
except KeyboardInterrupt:
    pass

finally:
    motor.disable(True)
    bus.close()
