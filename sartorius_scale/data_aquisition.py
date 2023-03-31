import numpy as np
import serial_ports_find
import mettler_toledo_device

scale = serial_ports_find.connect_scale()

if scale == None:
    scale = serial_ports_find.custom_connect_scale()

scale.ser.timeout = .1

print(scale.ser)

while(True):
    print(scale.read_screen().decode('utf-8'))

# scale = mettler_toledo_device.MettlerToledoDevice(port = "COM5")

# scale.get_commands()