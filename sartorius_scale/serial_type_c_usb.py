import matplotlib.pyplot as plt
import numpy as np
import serial

serial_port = 'COM4'
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

print(ser)

ser.close()




