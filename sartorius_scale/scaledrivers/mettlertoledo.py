import serial
from scaledrivers.scale import Scale
from data_class import Data

# Superclass for all Mettler Toledo scales

class MettlerToledo(Scale):

    def __init__(self, port):

        # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
        # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
        self.BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
        self.BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
        self.STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
        self.PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

        self.DEFAULT = {"baudrate": 9600, "bytesize": serial.EIGHTBITS, "stopbits": serial.STOPBITS_ONE, "parity": serial.PARITY_NONE}  # Tuple of Default configuration

        self.COMMAND_START = ''
        self.COMMAND_END = '\r\n'
        self.TARE = 'T'
        self.PRINT_SCREEN = 'SI'
        self.ZERO = 'Z'
        self.SOUND = 'M12'
        
        self.set_serial(port, self.DEFAULT)
        
    
    def get_weight_data(self):
        weight_string = self.send_receive(self.PRINT_SCREEN)
        # print(weight_string)  # For debugging
        weight_data = Data()
        if(weight_string[2] == 'S'):
            weight_data.stable = True
        weight_data.measure = float(weight_string[6:13])
        weight_data.unit = weight_string[15]
        return weight_data
    
# Dictionary of all scales by name
scales = {"XP205": MettlerToledo}