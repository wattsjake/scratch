import numpy as np
import serial_ports_find
import keyboard as kb

scale = serial_ports_find.connect_scale()

if scale != None:
    print(scale.ser)

    while(not kb.is_pressed("q")):
        print(scale.read())
        if kb.is_pressed("s"):
            scale.ser.write(b'S')
            print(scale.read())