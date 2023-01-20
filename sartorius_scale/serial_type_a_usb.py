import matplotlib.pyplot as plt
import numpy as np
import serial

ser = serial.Serial(port = 'COM7',
                    baudrate= 1200,
                    timeout = 5,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS)

while(True):
    print(ser.readline().decode('utf-8'))
    ser.close()




