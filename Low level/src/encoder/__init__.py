import machine
import utime as time
from machine import Pin 

class Encoder:
    """
    Encoder class that tracks an encoder using interruptions 
    PinA and PinB are integer numbers of the pins that are connected to the A and B channels from encoder
    
    Currently there is only one availvable method, that returns number of ticks from the initial position
    """

    def __init__(self, PinA, PinB):  

        self.ChA = Pin(PinA, Pin.IN, None)  # encoder channel A, PinA, no internal pull-up or pull-down resistor
        self.ChB = Pin(PinB, Pin.IN, None)  # encoder channel A, PinB, no internal pull-up or pull-down resistor
        self.enable_ChA_irq(self.update)
        self.enable_ChB_irq(self.update)
        self.state = (self.ChA.value() << 1) + self.ChB.value()
        self.position = 0 
        
    def enable_ChA_irq(self, callback=None):
        self.ChA.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

    def enable_ChB_irq(self, callback=None):
        self.ChB.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)

    def update(self, pin):
        new_state = (self.ChA.value() << 1) | self.ChB.value()
        if new_state == self.state:
            return

        transition = (self.state << 2) | new_state

        if transition == 0b1110:
            self.position += 1
        if transition == 0b1011:
            self.position -= 1
        self.state = new_state

    def get_pos(self):
        return self.position
        
     
if __name__ == "__main__":
  machine.freq(240000000)

  enc = Encoder(34, 35)
  count = 0

  while True:
    print(enc.get_pos())
    sleep(0.1)
