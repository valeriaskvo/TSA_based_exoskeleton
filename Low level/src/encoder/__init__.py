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
        """
        The __init__ function is called when the class is instantiated.
        It sets up the pins for use as encoder inputs, and initializes variables.
        
        :param self: Represent the instance of the class
        :param PinA: Specify the pin number of channel a
        :param PinB: Set the pin number of the encoder channel b
        :return: The object self, which is a reference to the instance of the class
        :doc-author: Trelent
        """
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
        """
        The update function is called when the encoder's state changes.
        The new_state variable holds the current state of the encoder, and transition holds a 4-bit value representing both states.
        If transition is 0b1110 or 0b1010, then we know that one full rotation occur. 
        We can use the information from which state to which to determine the direction we're turning.
        
        :param self: Represent the instance of the class
        :param pin: Determine which pin has changed
        :return: Nothing
        :doc-author: Trelent
        """
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
