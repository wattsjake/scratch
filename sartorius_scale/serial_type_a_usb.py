import matplotlib.pyplot as plt
import numpy as np
import serial
from scale_superclass import Scale

class Entris(Scale):



    def __init__(self, port):

        # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
        # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
        self.BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
        self.BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
        self.STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
        self.PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

        self.DEFAULT = (1200, serial.SEVENBITS, serial.STOPBITS_ONE, serial.PARITY_ODD)  # Tuple of Default configuration

        self.TARE = b'\x1BU'
        self.PRINT_SCREEN = b'\x1BP'
        self.ZERO = b'\x1Bf3_'
        self.SOUND = b'\x1BQ'
        
        self.ser = serial.Serial(port = port, 
                                 baudrate = self.DEFAULT[0], 
                                 bytesize = self.DEFAULT[1], 
                                 stopbits = self.DEFAULT[2], 
                                 parity = self.DEFAULT[3],
                                 timeout = 2)
        

# ser = serial.Serial(port = 'COM7',
#                     baudrate= 19200,
#                     timeout = 2,
#                     parity = serial.PARITY_ODD,
#                     stopbits = serial.STOPBITS_ONE,
#                     bytesize = serial.EIGHTBITS)

# while(True):
#     print(ser.readline().decode('utf-8'))
#     ser.close()




