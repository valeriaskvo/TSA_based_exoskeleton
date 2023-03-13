from machine import Pin, ADC, CAN

from can_interface import CanBus, encode


class ForceSensor:
    MAX_KILOGRAMS = 100
    MAX_ADC_VALUE = 65535

    def __init__(self, _id, pin, can: CAN) -> None:
        if isinstance(pin, int):
            self.sensor = ADC(Pin(pin))
        elif isinstance(pin, Pin):
            self.sensor = ADC(pin)
        else:
            raise ValueError(f"Pin: {type(pin)} type is not valid for ADC, only `int` / `Pin`")

        self.device_id = _id
        self.__can = CanBus(can)
        self.offset = self.__set_zero()

    def __buffer(self, n_reads: int = 100) -> float:
        buffer = [self.sensor.read_u16() for _ in range(n_reads)]
        return sum(buffer) / n_reads

    def __set_zero(self) -> float:
        return self.__buffer()

    def read(self, n_reads: int = 100) -> float:
        val = self.__buffer(n_reads)
        return self.MAX_KILOGRAMS * (val - self.offset) / self.MAX_KILOGRAMS

    def read_raw(self, n_reads: int = 100) -> int:
        val = self.__buffer(n_reads)
        return int(val - self.offset)

    def send(self, board_id: int) -> None:
        val = self.read_raw()
        self.__can.send(board_id, encode(self.device_id, [0, 0, val], data_to_byte=True))
