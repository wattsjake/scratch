import numpy as np
import serial_ports_find

scale = serial_ports_find.connect_scale()

if scale == None:
    scale = serial_ports_find.custom_connect_scale()

print(scale.ser)