import serial
from scaledrivers import scale
from data_class import Data

# Superclass for all Mettler Toledo scales

class MettlerToledo(scale.Scale):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    DEFAULT = {"baudrate": 9600, "bytesize": serial.EIGHTBITS, "stopbits": serial.STOPBITS_ONE, "parity": serial.PARITY_NONE}  # Tuple of Default configuration

    COMMAND_START = ''
    COMMAND_END = '\r\n'
    TARE = 'T'
    PRINT_SCREEN = 'SI'
    ZERO = 'Z'
    SOUND = 'M12'

    def __init__(self, port, **kwargs):
        scale.Scale.__init__(self, kwargs)
        self.set_serial(port, self.DEFAULT, kwargs)
    
    def get_weight_data(self):
        weight_string = self.send_receive(self.PRINT_SCREEN)
        string_end = len(weight_string) - len(self.COMMAND_END)
        weight_data = scale.string_to_measure(weight_string[4:string_end])
        if(weight_string[2] == 'S'):
            weight_data.stable = True
        return weight_data
    
# Dictionary of all scales by name
scales = {"XP205": MettlerToledo}