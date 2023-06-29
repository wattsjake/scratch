import serial
from scaledrivers import scale
from data_class import Data
import six

# Superclass for all Mettler Toledo scales
@six.add_metaclass(scale.custom_class_repr("Mettler Toledo"))
class MettlerToledo(scale.Scale):

    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
    BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
    STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
    PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

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
        """Gets weight data from a Mettler Toledo scale

        :raises scale.ScaleMeasurementException: If the scale is overloaded or underloaded
        :return: Measurement from the scale
        :rtype: data_class.Data
        """

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
        """Determines if a response from the scale is complete

        Mettler Toledo scales will indicate if a response has more lines by including a " B " in the response

        :param next_line: Next line of the response
        :type next_line: str
        :return: True if the response is complete, False otherwise
        :rtype: bool
        """

        return not " B " in next_line

    def test_port(self) -> bool:
        """Tests a port to see if it is a Mettler Toledo scale

        :return: True if the port is connected to a Mettler Toledo scale, False otherwise
        :rtype: bool
        """

        response = self.send_receive(self.SCALE_INFO)
        while response == "ES\r\n":     # Sometimes the scale starts by sending an error message
            response = self.send_receive(self.SCALE_INFO)
        response = response.split(" ")
        if len(response) < 2:
            return False
        return response[1] == "A"

    def __str__(self):
        return "Mettler Toledo"

scales = [MettlerToledo]  #: List of all Mettler Toledo scales