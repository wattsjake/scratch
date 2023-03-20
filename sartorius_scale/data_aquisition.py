import numpy as np
import serial_ports_find

scale = serial_ports_find.connect_scale()

if scale == None:
    scale = serial_ports_find.custom_connect_scale()

print(scale.ser)

while(True):
    print(scale.read_screen().decode('utf-8'))