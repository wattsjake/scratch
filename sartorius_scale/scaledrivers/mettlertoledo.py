import serial
from scaledrivers import scale
from data_class import Data
import six

# Superclass for all Mettler Toledo scales
@six.add_metaclass(scale.custom_class_repr("Mettler Toledo"))
class MettlerToledo(scale.Scale):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

    # Default settings for serial connection are the standard

    COMMAND_START = ''
    COMMAND_END = '\r\n'
    CANCEL = '@'
    TARE = 'T'
    PRINT_SCREEN = 'SI'
    ZERO = 'Z'
    SOUND = 'M12'
    SCALE_INFO = 'I2'
    RES_ERROR = 'ES'
    
    def get_weight_data(self):
        weight_string = self.send_receive(self.PRINT_SCREEN)
        match weight_string[2]:
            case '+':
                raise scale.ScaleMeasurementException("Scale is overloaded")
            case '-':
                raise scale.ScaleMeasurementException("Scale is underloaded")
        string_end = len(weight_string) - len(self.COMMAND_END)
        weight_data = scale.string_to_measure(weight_string[4:string_end])
        if(weight_string[2] == 'S'):
            weight_data.stable = True
        return weight_data
    
    def response_complete(self, next_line):
        return not " B " in next_line

    def test_port(self) -> bool:
        response = self.send_receive(self.SCALE_INFO)
        while response == "ES\r\n":
            response = self.send_receive(self.SCALE_INFO)
        response = response.split(" ")
        if len(response) < 2:
            return False
        return response[1] == "A"

    def __str__(self):
        return "Mettler Toledo"

# List of all scales
scales = [MettlerToledo]