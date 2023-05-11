import csv
import numpy as np
import serial 

import matplotlib.pyplot as plt
import numpy as np
from scale import Scale

class Entris_II(Scale):



    def __init__(self, port):

        # All possible settings for options required to initiate connection listed in case a brute force connection is necessary
        # Default configuration is 19200 baud, 8 data bits, 1 stop bit, odd parity
        self.BAUDRATES = (600, 1200, 2400, 4800, 9600, 19200)  # Tuple of possible baud-rates
        self.BYTESIZES = (serial.EIGHTBITS, serial.SEVENBITS)  # Tuple of possible byte sizes
        self.STOPBITS = (serial.STOPBITS_ONE, serial.STOPBITS_TWO)  # Tuple of possible stop bits
        self.PARITIES = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)  # Tuple of possible parities

        self.DEFAULT = (19200, serial.EIGHTBITS, serial.STOPBITS_ONE, serial.PARITY_ODD)  # Tuple of Default configuration

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
        

# tare = b'\x1BU'
# print_screen = b'\x1BP'
# zero = b'\x1Bf3_'
# sound = b'\x1BQ'

# def connect():
#     print('connecting to device')
#     try:
#         ser = serial.Serial(
#                             port='COM4',\
#                             baudrate=115200,\
#                             parity=serial.PARITY_NONE,\
#                             stopbits=serial.STOPBITS_ONE,\
#                             bytesize=serial.EIGHTBITS,\
#                             timeout=4)
#         print("connected to: " + ser.portstr)
    
#     except serial.serialutil.SerialException:
#         print("The port is in use. Unplug USB-C")  
#     return ser
  
# def serial_send(parameter,ser):
#     try:
#         ser.write(parameter)
#         print("Serial Send %s" %parameter)
#     except NameError as e:
#         print('[Error]Connect to scale')

# def main():
#     ser = connect()
#     ser.write(zero)
#     ser.write(sound)

#     while(True):
#         print(chr(ser.read()))
    

# if __name__ == "__main__":
#      main()


