import serial
from scaledrivers import scale
from scaledrivers.scale import Scale

class Sartorius(Scale):

    def __init__(self):
        if not hasattr(self, "TARE"):
            self.TARE = b'\x1BU'
        if not hasattr(self, "PRINT_SCREEN"):
            self.PRINT_SCREEN = b'\x1BP'
        if not hasattr(self, "ZERO"):
            self.ZERO = b'\x1Bf3_'
        if not hasattr(self, "SOUND"):
            self.TARE = b'\x1BQ'

class Entris(Sartorius):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    DEFAULT = {"baudrate": 1200, 
               "bytesize": serial.SEVENBITS, 
               "stopbits": serial.STOPBITS_ONE, 
               "parity": serial.PARITY_ODD}  # Tuple of Default configuration

    def __init__(self, port):
        
        self.set_serial(port, self.DEFAULT)

class EntrisII(Sartorius):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    DEFAULT = {"baudrate": 19200, 
               "bytesize": serial.EIGHTBITS, 
               "stopbits": serial.STOPBITS_ONE, 
               "parity": serial.PARITY_ODD}  # Dict of Default configuration

    def __init__(self, port):
        
        self.set_serial(port, self.DEFAULT)