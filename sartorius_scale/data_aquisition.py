import numpy as np
import serial_ports_find

scale = serial_ports_find.connect_scale()

print(scale.ser)