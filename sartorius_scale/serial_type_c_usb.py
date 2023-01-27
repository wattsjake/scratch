import matplotlib.pyplot as plt
import numpy as np
import serial
  
ser = serial.Serial("COM3", 
                     115200, 
                     timeout = 3, 
                     bytesize=serial.EIGHTBITS, 
                     parity=serial.PARITY_ODD,
                     stopbits=serial.STOPBITS_ONE)

#read from display
data = ser.read(100)
print(data)
