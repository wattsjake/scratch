import numpy as np
import serial_ports_find
import keyboard as kb
from serial.tools import miniterm

scale = serial_ports_find.connect_scale()

if scale != None:
    print(scale.ser)

    scale.ser.miniterm