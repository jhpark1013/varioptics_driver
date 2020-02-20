import serial
from serial import Serial, SerialException
from functools import partial

def get_port_from_serial_number(serial_number=None):
    from serial.tools.list_ports import comports
    available_comports = comports()
    serial_num_list = []
    for c in available_comports:
        serial_num_list.append(c.serial_number)
        if serial_number is None or c.serial_number == serial_number:
            return c

bytes_to_short = partial(int.from_bytes, byteorder='little', signed=True)
bytes_to_int32 = partial(int.from_bytes, byteorder='little', signed=True)
short_to_bytes = partial(int.to_bytes,
                         length=2, byteorder='little', signed=True)
long_to_bytes = partial(int.to_bytes,
                        length=4, byteorder='little', signed=True)
class Varioptics:

    def __init__(self, serial_number:str=None):
        self._serial_number = serial_number
        self._serial = None
        self.test = 11

    @staticmethod
    def list_available_serial_numbers():
        from serial.tools.list_ports import comports
        available_comports = comports()
        serial_num_list = []
        for c in available_comports:
            serial_num_list.append(c.serial_number)
        return serial_num_list

    def open(self):
        if self._serial is not None:
            return

        device = get_port_from_serial_number(serial_number=self._serial_number)
        self._serial_number = device.serial_number
        self._com = device.device
        self._serial = Serial(port=self._com) #SerialException: could not open port 'COM11': PermissionError(13, 'Access is denied.', None, 5)
        #self._serial = Serial()

        # try:
        #     self._serial = Serial(
        #         port=self._com, baudrate=self._baudrate, timeout=self._timeout,
        #         exclusive=self._exclusive)
        # except SerialException(
        #     "Must close previous connection with lens before establishing new one."
        #     "If there is a previous connection, call the 'close' method.")

    def close(self):
        self._serial.close()

    @property
    def serial_number(self):
        return self._serial_number

    def _write(self, command, param1=0x00, param2=0x00, param3=0x00, param4=0x00):
        """test with lens._write(0x0237, 0x03, 0x01, 0xFF, 0x3C)"""
        """after writing, read the response to see if transaction is successful"""
        command = (short_to_bytes(command) +
                    bytes([param1 & 0xFF, param2 & 0xFF, param3 & 0xFF, param4 & 0xFF]))
        self._serial.write(command)

    def _read(self):
        """if write 0x0237 was successful, ack (the 3rd byte) will be 0x06"""
        """if unsuccessful, it will be 0x15"""
        b = self._serial.read(4)
        command = bytes_to_short(b[0:1])
        param1 = int(b[2])
        param2 = int(b[3])
        return (param1, param2)
