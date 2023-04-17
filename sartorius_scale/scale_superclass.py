import serial
import time
import mettler_toledo_device

class Scale:

    # This was made by Noah Mazza.
    def __init__(self):
        if not 'PRINT_SCREEN' in locals():
            self.set_print_screen(b'SI\r\n')  # For testing Mettler Toledo scales

    # def __init__(self, port_, baudrate_, bytesize_, stopbits_, parity_, timeout_):
    #     self.ser = serial.Serial(port = port_, baudrate = baudrate_, bytesize = bytesize_, stopbits = stopbits_, parity = parity_, timeout = timeout_)
    #     return self

    # # # SETTERS # # #
    # Used for making a generic scale class in the future.



    def set_baudrates(self, baudrates):
        self.BAUDRATES = baudrates

    def set_bytesizes(self, bytesizes):
        self.BYTESIZES = bytesizes

    def set_stopbits(self, stopbits):
        self.STOPBITS = stopbits

    def set_parities(self, parities):
        self.PARITIES = parities

    def set_tare(self, tare):
        self.TARE = tare

    def set_print_screen(self, print_screen):
        self.PRINT_SCREEN = print_screen

    def set_zero(self, zero):
        self.ZERO = zero

    def set_sound(self, sound):
        self.SOUND = sound

    def set_serial(self, port_, baudrate_, bytesize_, stopbits_, parity_, timeout_):
        self.ser = serial.Serial(port = port_, baudrate = baudrate_, bytesize = bytesize_, stopbits = stopbits_, parity = parity_, timeout = timeout_)
        return self


    # # # GETTERS # # #
    # Will fill in later as needed


    # # # METHODS # # #

    # This method is used to send a command to the scale and receive a response.
    # After sending a command, the response has to be read or else miscommunication will occur.
    def send_receive(self, command):
        self.ser.write(command)
        return self.ser.readline()



    # All of this was generated with GitHub Copilot.  We'll see if it works.



    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()

    def read_screen(self):
        return self.send_receive(self.PRINT_SCREEN)

    def zero(self):
        return self.send_receive(self.ZERO)

    def tare(self):
        return self.send_receive(self.TARE)

    def sound(self):
        return self.send_receive(self.SOUND)

    def get_info(self):
        self.ser.write(b'V\r')
        return self.ser.readline()

    def get_stability(self):
        self.ser.write(b'S\r')
        return self.ser.readline()

    def get_units(self):
        self.ser.write(b'U\r')
        return self.ser.readline()

    def get_mass(self):
        self.ser.write(b'P\r')
        return self.ser.readline()

    def get_status(self):
        self.ser.write(b'ST\r')
        return self.ser.readline()

    def get_error(self):
        self.ser.write(b'ER\r')
        return self.ser.readline()

    def get_battery(self):
        self.ser.write(b'BT\r')
        return self.ser.readline()

    def get_temperature(self):
        self.ser.write(b'TM\r')
        return self.ser.readline()

    def get_calibration(self):
        self.ser.write(b'CL\r')
        return self.ser.readline()

    def get_calibration_date(self):
        self.ser.write(b'CD\r')
        return self.ser.readline()

    def get_calibration_time(self):
        self.ser.write(b'CT\r')
        return self.ser.readline()

    def get_calibration_user(self):
        self.ser.write(b'CU\r')
        return self.ser.readline()

    def get_calibration_weight(self):
        self.ser.write(b'CW\r')
        return self.ser.readline()

    def get_calibration_weight_units(self):
        self.ser.write(b'CU\r')
        return self.ser.readline()