import matplotlib.pyplot as plt
import numpy as np
import serial

class Entris:
    
    # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
    # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
    BAUD_RATES = [600, 1200, 2400, 4800, 9600, 19200]  # List of possible baud-rates
    BYTESIZES = [serial.EIGHTBITS, serial.SEVENBITS]  # List of possible byte sizes
    STOPBITS = [serial.STOPBITS_ONE, serial.STOPBITS_TWO]  # List of possible stop bits
    PARITIES = [serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN]  # List of possible parities

    DEFAULT = [19200, serial.EIGHTBITS, serial.STOPBITS_ONE, serial.PARITY_ODD]  # Default configuration

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




