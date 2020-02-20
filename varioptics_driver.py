def _get_port_from_serial_number():


class Varioptics:

    def __init__(self, serial_number:str=none):
        self._serial_number = serial_number

    @staticmethod
    def list_available_serial_numbers():
        from serial.tools.list_ports import available_comports
        available_comports = comports()
        serial_num_list = []
        for c in available_comports:
            serial_num_list.append(c.serial_number)
        return serial_num_list
