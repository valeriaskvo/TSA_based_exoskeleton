from time import sleep
from machine import SoftI2C, ADC, Pin
from IMU import IMU

def generate_msg(vals, msg=""):
    for key in vals:
        if key == "Tmp":
            continue
        if msg == "":
            msg = str(vals[key])
        else:
            msg += " " + str(vals[key])
    return msg

# IMU
i2c_1 = SoftI2C(scl=Pin(22), sda=Pin(21)) 
imu_1 = IMU(i2c_1, imu_id=1)

i2c_2 = SoftI2C(scl=Pin(19), sda=Pin(18))
imu_2 = IMU(i2c_2, imu_id=2)

# Analog IN
adc = ADC(Pin(12))
val = adc.read_u16()

while True:
    imu_d1 = imu_1.get_data()
    msg = generate_msg(imu_d1)
    imu_d2 = imu_2.get_data()
    msg = generate_msg(imu_d2, msg)
    force = adc.read_u16()
    msg += " " + str(force)
    print(msg)
    
    sleep(0.0001)
