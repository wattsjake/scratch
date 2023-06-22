import serial
from scaledrivers import scale
import six

# Superclass for all Sartorius scales
@six.add_metaclass(scale.custom_class_repr("Sartorius"))
class Sartorius(scale.Scale):

    COMMAND_START = '\x1B'
    COMMAND_END = ''

    def __init__(self, port: str, **kwargs):
        if not hasattr(self, "TARE"):
            self.TARE = 'U'
        if not hasattr(self, "PRINT_SCREEN"):
            self.PRINT_SCREEN = 'P'
        if not hasattr(self, "ZERO"):
            self.ZERO = 'f3_'
        if not hasattr(self, "SOUND"):
            self.TARE = 'Q'
        if not hasattr(self, "SCALE_INFO"):
            self.SCALE_INFO = 'x1_'

        scale.Scale.__init__(self, port, **kwargs)

    def __str__(self):
        return "Sartorius"
    
    def test_port(self):
        response = self.send_receive(self.SCALE_INFO)
        return False  # Not yet implemented

    def response_complete(self, next_line):
        return True  # Not yet implemented

@six.add_metaclass(scale.custom_class_repr("Entris", Sartorius))
class Entris(Sartorius):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    DEFAULT_SERIAL = {"baudrate": 1200, 
               "bytesize": serial.SEVENBITS, 
               "stopbits": serial.STOPBITS_ONE, 
               "parity": serial.PARITY_ODD}  # Dict of Default configuration
    
    def __str__(self):
        return "Entris"

@six.add_metaclass(scale.custom_class_repr("Entris II", Sartorius))
class EntrisII(Sartorius):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    DEFAULT_SERIAL = {"baudrate": 19200, 
               "bytesize": serial.EIGHTBITS, 
               "stopbits": serial.STOPBITS_ONE, 
               "parity": serial.PARITY_ODD}  # Dict of Default configuration
    
    def __str__(self):
        return "Entris II"

# List of all scales
scales = [Entris, EntrisII]