import serial
from scale import Scale
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

        self.TARE = b'T\r\n'
        self.PRINT_SCREEN = b'SI\r\n'
        self.ZERO = b'Z\r\n'
        self.SOUND = b'M12\r\n'
        
        self.ser = serial.Serial(port = port, 
                                 baudrate = self.DEFAULT["baudrate"], 
                                 bytesize = self.DEFAULT["bytesize"], 
                                 stopbits = self.DEFAULT["stopbits"], 
                                 parity = self.DEFAULT["parity"], 
                                 timeout = 2)
        
    
    def get_weight_data(self):
        self.ser.write(self.PRINT_SCREEN)
        weight_string = self.ser.readline().decode('utf-8')
        # print(weight_string)  # For debugging
        weight_data = Data()
        if(weight_string[2] == 'S'):
            weight_data.stable = True
        weight_data.measure = float(weight_string[6:13])
        weight_data.unit = weight_string[15]
        return weight_data