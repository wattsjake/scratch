import matplotlib.pyplot as plt
import numpy as np
import serial
from scale_superclass import Scale

class Entris(Scale):



    def __init__(self):

        # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
        # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
        # [TODO] Change all of these variable assignments to use setter methods in the superclass
        # [TODO] Store all of the values here as constants outside of init
        super().BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
        super().BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
        super().STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
        super().PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

        super().DEFAULT = (19200, serial.EIGHTBITS, serial.STOPBITS_ONE, serial.PARITY_ODD)  # Tuple of Default configuration

        super().TARE = b'\x1BU'
        super().PRINT_SCREEN = b'\x1BP'
        super().ZERO = b'\x1Bf3_'
        super().SOUND = b'\x1BQ'
        

    # [TODO] Add default values for communicating with the scale (read weight, tare, change settings)

ser = serial.Serial(port = 'COM7',
                    baudrate= 19200,
                    timeout = 2,
                    parity = serial.PARITY_ODD,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS)

while(True):
    print(ser.readline().decode('utf-8'))
    ser.close()




