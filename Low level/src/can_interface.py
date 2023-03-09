from machine import CAN


def encode(
    device_id: int,
    data: list,
    *,
    device_flag: int = 0x00,
    data_to_byte: bool = False,
    byte_order: str = "little",
    signed: bool = True
) -> list:
    """
    The encode function takes a device ID, a list of data elements, and some optional parameters.
    It returns an encoded message in the form of a list of bytes. The first byte is always the device ID.
    The second byte is always 0x00 to indicate that this message contains no flags for special functions.
    The third through sixth bytes are padded with nulls to ensure that there are six total bytes in
    the payload (since we don't send more than three integers). The remaining four or eight bytes contain
    the data elements as integer values.

    :param device_id:int: Identify the device that sends the data
    :param data:list: Send data to the device
    :param *: Pass a variable number of arguments to a function
    :param device_flag:int=0x00: Set the device flag
    :param data_to_byte:bool=False: Determine whether the data should be converted to bytes or not
    :param byte_order:str="little": Specify the byte order of the data
    :param signed:bool=True: Determine if the bytes should be interpreted as signed or unsigned
    :return: A byte array
    :doc-author: Trelent
    """
    if len(data) > 6 and not data_to_byte:
        raise ValueError("Data array should be not longer than 6 bytes")

    if len(data) > 3 and data_to_byte:
        raise ValueError("Data array should be not longer than 3 integer elements")

    message = [device_id, device_flag]

    if not data_to_byte:
        nulls = [0x00] * (6 - len(data))
        message.extend(nulls)
        message.extend(data)

        return message

    nulls = [0x00] * (3 - len(data)) * 2
    message.extend(nulls)
    for item in data:
        b = int.to_bytes(item, 2, byteorder=byte_order, signed=signed)
        message.extend(list(b))
    return message


class CanBus:

    def __init__(self, can: CAN) -> None:
        self._can = can
        self._can.clear_rx_queue()
        self._can.clear_tx_queue()

    def __del__(self) -> None:
        self._can.clear_rx_queue()
        self._can.clear_tx_queue()
        self._can.deinit()

    def send(self, board_id: int, data: list) -> None:
        self._can.send(data, board_id)
        self._can.clear_rx_queue()
        self._can.clear_tx_queue()
