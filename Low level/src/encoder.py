from machine import Pin, CAN
from can_interface import CanBus, encode

class Encoder:

    def __init__(self, _id, PinA: int, PinB: int, can: CAN):
        self.ChA = Pin(PinA, Pin.IN, None)  # encoder channel A, PinA, no internal pull-up or pull-down resistor
        self.ChB = Pin(PinB, Pin.IN, None)  # encoder channel A, PinB, no internal pull-up or pull-down resistor
        self.enable_ChA_irq(self.update)
        self.enable_ChB_irq(self.update)
        self.state = (self.ChA.value() << 1) + self.ChB.value()
        self.position = 0
        self.device_id = _id
        self.__can = CanBus(can)

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

    def send(self, board_id: int):
        val = self.get_pos()
        self.__can.send(board_id, encode(self.device_id, [0, 0, val], data_to_byte=True))
